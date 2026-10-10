# EC2 and device experiment guide

This guide is preparatory. It does not download or execute a paper-level experiment.

1. Create a private EC2 project volume and Python 3.11 environment. Install this package from a pinned repository commit.
2. Manually accept licenses/register for benchmarks and place files under the layout in `data_format.md`.
3. Manually clone external agent/benchmark repositories at audited commits. Do not let configuration files execute arbitrary shell commands.
4. Build the four open synthetic-secret test applications and isolated verifier/attacker endpoints. Record source and APK hashes.
5. Provision the Pixel userdebug build and, if used, the Samsung device. Record AOSP/build/kernel, boot state, Keystore security level, and OEM limitations.
6. Implement `AospAdapter`, `PlatformFlowAdapter`, `AgentRunnerAdapter`, and `BenchmarkAdapter` in a separate integration module. Add contract tests before device runs.
7. Copy `configs/experiment_template.yaml`; set only already-provisioned paths and registered device/agent IDs. Freeze all Table D.6 parameters before inspecting outcomes.
8. Run one isolated canary smoke test. Confirm no production account, OTP, address, credential, or payment data is present.
9. Run the killer experiment before expanding the matrix. A failure of exposure, redirection denial, or legitimate completion blocks the corresponding claim.
10. Run paired trials, record every exclusion, export raw secret-free outcomes, and generate tables/plots only from those files.

Credentials belong in the external runner's secret manager or environment, never YAML, logs, repository files, or provenance exports.
