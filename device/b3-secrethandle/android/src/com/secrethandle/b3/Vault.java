package com.secrethandle.b3;

import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * In-memory secret vault for SecretHandle.
 *
 * Implements Algorithm 1 (Mint) and Algorithm 2 (Resolve) from the paper:
 * - Opaque handle generation (SH-XXXXXX)
 * - Single-use consumption (Replay protection)
 * - Time-to-live expiration (TTL = 5 minutes)
 * - Destination and task binding verification
 */
public final class Vault {

    public static final long TTL_MS = 5 * 60 * 1000L;

    public static final class Entry {
        public final String handle;
        public final String secret;
        public final String source;
        public final String target;
        public final String targetOrigin;
        public final String targetField;
        public final long createdAt;
        public final long expiresAt;
        public int budget;
        public int remainingUses;
        public boolean used;

        Entry(String handle, String secret, String source, String target, String targetOrigin, String targetField, long expiresAt, int budget) {
            this.handle = handle;
            this.secret = secret;
            this.source = source;
            this.target = target;
            this.targetOrigin = targetOrigin;
            this.targetField = targetField;
            this.createdAt = System.currentTimeMillis();
            this.expiresAt = expiresAt;
            this.budget = budget;
            this.remainingUses = budget;
            this.used = false;
        }

        Entry(String handle, String secret, String source, String target, String targetField, long expiresAt, int budget) {
            this(handle, secret, source, target, null, targetField, expiresAt, budget);
        }

        Entry(String handle, String secret, String source, String target, String targetField, long expiresAt) {
            this(handle, secret, source, target, null, targetField, expiresAt, 1);
        }

        Entry(String handle, String secret, String source, String target, long expiresAt) {
            this(handle, secret, source, target, null, null, expiresAt, 1);
        }

        public boolean expired() {
            return System.currentTimeMillis() > expiresAt;
        }
    }

    private static final Map<String, Entry> ENTRIES = new LinkedHashMap<String, Entry>();
    private static final SecureRandom RNG = new SecureRandom();

    private Vault() {
    }

    public static synchronized String mint(String secret, String source, String target, String targetField) {
        StringBuilder sb = new StringBuilder("SH-");
        for (int i = 0; i < 6; i++) {
            sb.append("0123456789ABCDEF".charAt(RNG.nextInt(16)));
        }
        String handle = sb.toString();
        // A secret seen twice keeps its first handle if still valid
        for (Entry e : ENTRIES.values()) {
            if (e.secret.equals(secret) && !e.expired()) {
                return e.handle;
            }
        }
        ENTRIES.put(handle, new Entry(handle, secret, source, target, targetField, System.currentTimeMillis() + TTL_MS));
        return handle;
    }

    public static synchronized String mintWeb(String secret, String source, String target, String targetOrigin, String targetField) {
        StringBuilder sb = new StringBuilder("SH-WEB-");
        for (int i = 0; i < 4; i++) {
            sb.append("0123456789ABCDEF".charAt(RNG.nextInt(16)));
        }
        String handle = sb.toString();
        for (Entry e : ENTRIES.values()) {
            if (e.secret.equals(secret) && !e.expired()) {
                return e.handle;
            }
        }
        ENTRIES.put(handle, new Entry(handle, secret, source, target, targetOrigin, targetField, System.currentTimeMillis() + TTL_MS, 1));
        return handle;
    }

    public static synchronized String mint(String secret, String source, String target) {
        return mint(secret, source, target, null);
    }

    public static synchronized String mint(String secret, String source) {
        return mint(secret, source, null, null);
    }

    /**
     * Resolves a handle with destination binding check (Algorithm 2).
     * Enforces both Package binding and Field-Class binding (intra-app redirection defense).
     * Returns null if handle is unknown, expired, already used, or destination mismatches.
     * Leaves handle live (used remains false) on mismatch to prevent DoS.
     */
    public static synchronized String reveal(String handle, String callerPackage, String callerField) {
        Entry e = ENTRIES.get(handle);
        if (e == null) {
            return null; // Unknown handle
        }
        if (e.expired()) {
            ENTRIES.remove(handle);
            return null; // Expired
        }
        if (e.used || e.remainingUses <= 0) {
            return null; // Replay attack prevented or budget exhausted
        }
        // Destination package binding verification:
        if (e.target != null && callerPackage != null && !e.target.equals(callerPackage)) {
            return null; // Cross-app redirection attempt rejected!
        }
        // Destination field-class binding verification (intra-app redirection defense):
        if (e.targetField != null && callerField != null && !e.targetField.equals(callerField)) {
            return null; // Intra-app field redirection attempt rejected!
        }
        e.remainingUses--;
        if (e.remainingUses <= 0) {
            e.used = true;
        }
        return e.secret;
    }

    public static synchronized String reveal(String handle, String callerPackage) {
        return reveal(handle, callerPackage, null);
    }

    public static synchronized String revealWeb(String handle, String callerPackage, String callerOrigin, String callerField) {
        Entry e = ENTRIES.get(handle);
        if (e == null) {
            return null; // Unknown handle
        }
        if (e.expired()) {
            ENTRIES.remove(handle);
            return null; // Expired
        }
        if (e.used || e.remainingUses <= 0) {
            return null; // Replay attack prevented or budget exhausted
        }
        // Package binding check
        if (e.target != null && callerPackage != null && !e.target.equals(callerPackage)) {
            return null; // Package mismatch rejected
        }
        // Origin binding check: Fail-closed on unattested or mismatched origins (Section 4.2 & Definition 5.1)
        if (e.targetOrigin != null) {
            if (callerOrigin == null || !e.targetOrigin.equalsIgnoreCase(callerOrigin)) {
                return null; // Fail-closed: origin unattested or mismatched!
            }
        }
        // Field-class check
        if (e.targetField != null && callerField != null && !e.targetField.equals(callerField)) {
            return null; // Field mismatch rejected
        }
        e.remainingUses--;
        if (e.remainingUses <= 0) {
            e.used = true;
        }
        return e.secret;
    }

    /**
     * Fallback Policy for Custom Canvas / Flutter / React Native numpads (Section 4.3):
     * Enforces foreground package identity verification and single-tap user touch confirmation.
     */
    public static synchronized String revealFallback(String handle, String foregroundPackage, boolean userTouchConfirmed) {
        Entry e = ENTRIES.get(handle);
        if (e == null) {
            return null;
        }
        if (e.expired()) {
            ENTRIES.remove(handle);
            return null;
        }
        if (e.used || e.remainingUses <= 0) {
            return null;
        }
        // Step 1: Verified foreground package identity check
        if (e.target != null && (foregroundPackage == null || !e.target.equals(foregroundPackage))) {
            return null; // Cross-app fallback attempt rejected immediately!
        }
        // Step 2: Single-tap user touch confirmation verification
        if (!userTouchConfirmed) {
            return null; // Touch confirmation missing
        }
        e.remainingUses--;
        if (e.remainingUses <= 0) {
            e.used = true;
        }
        return e.secret;
    }

    public static synchronized String reveal(String handle) {
        return reveal(handle, null, null);
    }

    public static synchronized String mintWithBudget(String secret, String source, String target, int budget) {
        StringBuilder sb = new StringBuilder("SH-CLIP-");
        for (int i = 0; i < 4; i++) {
            sb.append("0123456789ABCDEF".charAt(RNG.nextInt(16)));
        }
        String handle = sb.toString();
        ENTRIES.put(handle, new Entry(handle, secret, source, target, null, System.currentTimeMillis() + TTL_MS, budget));
        return handle;
    }

    /** Explicitly mint an expired entry for testing expiry lifecycle */
    public static synchronized String mintExpiredForTest(String secret, String source, String target) {
        StringBuilder sb = new StringBuilder("SH-EXP-");
        for (int i = 0; i < 4; i++) {
            sb.append("0123456789ABCDEF".charAt(RNG.nextInt(16)));
        }
        String handle = sb.toString();
        ENTRIES.put(handle, new Entry(handle, secret, source, target, System.currentTimeMillis() - 1000L));
        return handle;
    }

    public static synchronized boolean containsSecret(String text) {
        if (text == null || text.isEmpty()) {
            return false;
        }
        long now = System.currentTimeMillis();
        for (Entry e : ENTRIES.values()) {
            if (now <= e.expiresAt && text.contains(e.secret)) {
                return true;
            }
        }
        return false;
    }

    public static synchronized boolean isHandle(String text) {
        return text != null && ENTRIES.containsKey(text.trim());
    }

    public static synchronized List<Entry> entries() {
        long now = System.currentTimeMillis();
        List<Entry> out = new ArrayList<Entry>();
        for (Entry e : ENTRIES.values()) {
            if (now <= e.expiresAt) {
                out.add(e);
            }
        }
        return out;
    }

    public static synchronized void clear() {
        ENTRIES.clear();
    }
}
