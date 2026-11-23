# Azrim social design kit
Render: `npm i && python3 c01_v2.py` (needs playwright + Chrome). Logo/photo paths point at ../img.
Rules: paper #EFEBE1 / ink #151515 / gold #C9A84C / proof-red #D8432A (annotations only).
Fonts: Anton (display), Instrument Serif (headlines/italic accent), Inter Tight (body), Space Mono (meta/receipts), Caveat (handwritten notes).
Gold thread: every cover enters left edge and exits right edge at y=1215 (of 1350), stroke 7px, so covers connect across the Instagram/TikTok grid. Inside the cover it morphs to match the series.
Output: 1080x1350 JPEG to /social/YYYY-MM/MMDD-<id>-<n>.jpg
Pinned-row signature: the 3 pinned posts carry "Azrim Studio" in Allura script on the gold thread (split Az | rim Stu | dio). Language rotation for later pinned trios: Hungarian, Arabic, English, Persian, Russian, German, Chinese.
Reel covers 1080x1920: thread at y=1536 (aligns with y=1215 of 4:5 covers in the 3:4 grid crop).
Signature is monoline: script glyphs reduced to centre-line and redrawn at the thread's 7px width (monosig.py, needs scikit-image, brotli).
threadword.py: the thread flows into each word along the stroke's own direction (skeleton end-point tangents) and out again; no line runs under the letters.

## Publishing routes
- Instagram: OttoKit `custom_api_request` → Graph API v21.0, IG user 17841447605634432 (carousel: children with is_carousel_item, then CAROUSEL container, then media_publish).
- TikTok (@azrim.studio): OttoKit `execute_integration_action`, integration `tiktok_new_integration`, connection_id 168280. Media must be on OttoKit's domain first: `Convert_To_File` / `convert_to_file_move_base64_string_to_file_cloned_usigxu` (url → ottokit-files S3 url). Then `tiktok_post_photo` (photo_images list) or `tiktok_post_video` (video_url), privacy_level PUBLIC_TO_EVERYONE.
