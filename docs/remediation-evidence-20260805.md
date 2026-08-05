# Exhaustive production-audit remediation boundary

- Production remains unchanged at `a729d9f1df31acd9835bad9ee7b78408bf3d9672`.
- The corrected source boundary before this evidence commit is `5529e6b23197c16b9d3d944246e13ec128483a78`.
- PR #16 remains draft and unmerged.

## Corrections committed

1. Responsive navigation now locks the page without discarding the original scroll position and restores that position after closure.
2. The homepage responsive panel is explicitly viewport-bound at tablet, mobile and narrow-mobile widths.
3. Generated form-error IDs are removed from `aria-describedby` when validation errors are cleared.
4. Confirmed contrast failures and undersized interactive targets receive final cascade corrections.
5. Generated footer image markup is normalized to valid HTML.
6. SMTP subjects use an ASCII separator rather than an unencoded Unicode em dash.
7. Stable asset URLs use revalidation rather than a one-year immutable cache policy.
8. Runtime metadata is pinned to Node `20.x`, with `.nvmrc` and `.node-version` included.
9. Superseded phone, address and raster-logo references are removed from source inputs.
10. A permanent remediation validator enforces these contracts during normal validation.

## Required proof before approval

- exact-head Website CI;
- corrected preview deployment from the exact PR head;
- repeat of the 35-route full-page and overlapping-scroll audit;
- repeat of the real-pointer responsive-navigation matrix;
- repeat of desktop dropdown, form, accessibility, cross-browser and delivery checks;
- manual page-by-page sign-off with zero unresolved findings.

No merge or production deployment is authorized by this evidence record.
