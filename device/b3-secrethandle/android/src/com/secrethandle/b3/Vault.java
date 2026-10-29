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
        public final String targetField;
        public final long createdAt;
        public final long expiresAt;
        public boolean used;

        Entry(String handle, String secret, String source, String target, String targetField, long expiresAt) {
            this.handle = handle;
            this.secret = secret;
            this.source = source;
            this.target = target;
            this.targetField = targetField;
            this.createdAt = System.currentTimeMillis();
            this.expiresAt = expiresAt;
            this.used = false;
        }

        Entry(String handle, String secret, String source, String target, long expiresAt) {
            this(handle, secret, source, target, null, expiresAt);
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
        if (e.used) {
            return null; // Replay attack prevented
        }
        // Destination package binding verification:
        if (e.target != null && callerPackage != null && !e.target.equals(callerPackage)) {
            return null; // Cross-app redirection attempt rejected!
        }
        // Destination field-class binding verification (intra-app redirection defense):
        if (e.targetField != null && callerField != null && !e.targetField.equals(callerField)) {
            return null; // Intra-app field redirection attempt rejected!
        }
        e.used = true;
        return e.secret;
    }

    public static synchronized String reveal(String handle, String callerPackage) {
        return reveal(handle, callerPackage, null);
    }

    public static synchronized String reveal(String handle) {
        return reveal(handle, null, null);
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
