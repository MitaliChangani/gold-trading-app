# MetaGold Django - Ready to deploy
Date: 2025-08-14

This repo is a minimal Django project with:
- User signup/login (session-based)
- Wallet and Transactions
- Withdrawal requests (admin approve/reject)
- Razorpay order creation & payment verification endpoints
- Admin panel at /admin/

How to use:
1. Create GitHub repo and push these files.
2. Set environment variables (in Render or your host):
   - DJANGO_SECRET_KEY (e.g. a random string)
   - RAZORPAY_KEY_ID
   - RAZORPAY_KEY_SECRET
   - ALLOWED_HOSTS (comma separated, e.g. "*")
3. On first run:
   - python manage.py migrate
   - python manage.py createsuperuser (to access admin)
4. Deploy using Render (render.yaml included).

NOTE: This is a starting template. For production, add HTTPS, email verification, stronger auth, and monitoring.