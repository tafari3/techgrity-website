# Exhaustive production-audit remediation boundary

- Production remains unchanged at `a729d9f1df31acd9835bad9ee7b78408bf3d9672`.
- The corrected source boundary before this evidence update is `5c9d86a559fef88195e80f9e1992361452679f4b`.
- PR #16 remains draft and unmerged.

## Corrections committed

1. Responsive navigation locks the page without discarding the original scroll position and restores that position after closure.
2. The homepage responsive panel is explicitly viewport-bound at tablet, mobile and narrow-mobile widths.
3. Generated form-error IDs are removed from `aria-describedby` when validation errors are cleared.
4. Confirmed contrast failures and undersized interactive targets receive final cascade corrections.
5. Generated footer image markup is normalized to valid HTML.
6. SMTP subjects use an ASCII separator rather than an unencoded Unicode em dash.
7. Stable asset URLs use revalidation rather than a one-year immutable cache policy.
8. Runtime metadata is pinned to Node `24.x`, with `.nvmrc`, `.node-version`, a permanent Node 24 proof workflow and Vercel-compatible runtime validation.
9. Superseded phone, address and raster-logo references are removed from source inputs.
10. A permanent remediation validator enforces these contracts during normal validation.
11. The one-shot remediation workflow and patch script were retired after successful application so they cannot rerun or reintroduce obsolete settings.

## Runtime correction discovered during preview commissioning

The first corrected preview built successfully from `9696b88026115164ab670c75d7aa4f7331fe4de7` and rendered all 35 routes, but Vercel warned that Node 20 deployments created on or after 1 October 2026 will fail. The durable runtime boundary was therefore corrected to Node 24 before final preview certification.

## Required proof before approval

- exact-head Website CI;
- exact-head Node 24 runtime proof;
- corrected Node 24 preview deployment from the exact PR head;
- repeat of the 35-route full-page and overlapping-scroll audit against that preview;
- repeat of the real-pointer responsive-navigation matrix;
- repeat of desktop dropdown, form, accessibility, cross-browser and delivery checks;
- manual page-by-page sign-off with zero unresolved findings.

No merge or production deployment is authorized by this evidence record.
