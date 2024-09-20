source venv/bin/activate
python3 /home/aleon/odoo17/venv/lib/python3.12/site-packages/debugpy --listen 0.0.0.0:5678 ./odoo-bin --addons-path="addons/,tutorials/" -d rd-demo -u estate --dev xml