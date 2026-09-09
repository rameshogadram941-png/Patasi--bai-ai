Netlify deployment guide — Patasi Bai AI

I pushed netlify.toml to branch: patasi-bai-ai-co. Follow these steps to connect and deploy on Netlify (one minute):

1) Connect repo in Netlify UI
- Go to https://app.netlify.com/sites -> "Add new site" -> "Import from Git" -> Connect to GitHub
- Select repository: rameshogadram941-png/Patasi--bai-ai and branch: patasi-bai-ai-co

2) Build settings (use these exact values)
- Build command: npm run build
- Publish directory: .next
- Base directory: leave blank (root)

3) Environment variables (Site settings → Build & deploy → Environment)
Add the following (replace placeholders with real values):
- NODE_ENV=production
- DATABASE_URL=postgres://user:pass@host:5432/dbname
- RAZORPAY_KEY_ID=replace
- RAZORPAY_KEY_SECRET=replace
- MODEL_API_KEY=replace
- TWILIO_ACCOUNT_SID=replace
- TWILIO_AUTH_TOKEN=replace
- TWILIO_WHATSAPP_FROM=replace
- REDIS_URL=replace
- S3_BUCKET=replace
- S3_KEY=replace
- S3_SECRET=replace

If your build needs fewer vars, add only those required at build time. Missing env vars are the most common cause of build failures.

4) Netlify Next.js plugin
- netlify.toml references @netlify/plugin-nextjs. Netlify will auto-install it during build. If you prefer, run locally: npm install --save-dev @netlify/plugin-nextjs and commit package-lock.json.

5) Trigger deploy
- After connecting, click "Deploy site". Watch logs in Netlify UI: Site -> Deploys -> click the running deploy -> Logs.

6) Common fixes (if deploy fails)
- "Missing script: build" — ensure package.json has "build": "next build".
- "Module not found / build error" — check stack trace in deploy logs; add missing packages to package.json and push.
- ".next not found" — confirm you use Next.js and build command above. If you use next export, change publish dir to "out" and build to "next build && next export".
- "Environment variable missing" — add required env vars in Site settings and re-deploy.

7) Static vs SSR notes
- Netlify supports Next.js features via the plugin, but heavy server‑side features (long‑running sockets, WebSocket servers) may need a server platform (Vercel or Kubernetes). API routes will run as serverless functions.

8) If you want CI-driven deploy instead
- I can add a GitHub Actions workflow that runs npm ci, builds and deploys to Netlify using NETLIFY_AUTH_TOKEN and NETLIFY_SITE_ID repo secrets. Reply: "Add Netlify Action" and I will push it.

I will monitor the first deploy if you tell me when you click Deploy. If it fails, paste the deploy log or the deploy URL and I will diagnose and fix immediately.

Next step for you: click Deploy on Netlify or reply here "I clicked Deploy" and I’ll watch logs and guide the fixes live.
