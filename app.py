from flask import Flask, render_template, request

app = Flask(__name__)

def parse_main_wallets(data):
    """Parse main wallet data to extract wallet addresses and their conditions."""
    wallets = {}
    for line in data.strip().splitlines():
        try:
            # Split the wallet and condition
            wallet, condition = line.split()
            wallets[wallet.strip()] = condition.strip().lower()  # Normalize to lowercase
        except ValueError:
            continue
    return wallets

def validate_referrals(main_wallets, referral_wallets):
    """Validate referral wallets against main wallet conditions."""
    valid_referrals = []
    invalid_referrals = []

    for referral in referral_wallets:
        normalized_referral = referral.strip().lower()
        if normalized_referral in main_wallets and main_wallets[normalized_referral] == "20uxuy":
            valid_referrals.append(referral)
        else:
            invalid_referrals.append(referral)

    return valid_referrals, invalid_referrals

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get data from the form
    main_wallet_data = request.form.get('main_wallet_data', "")
    referral_wallet_data = request.form.get('referral_wallet_data', "")

    # Parse and validate wallets
    main_wallets = parse_main_wallets(main_wallet_data)
    referral_wallets = [line.strip() for line in referral_wallet_data.strip().splitlines()]
    valid_referrals, invalid_referrals = validate_referrals(main_wallets, referral_wallets)

    # Pass the results to the results template
    return render_template(
        'results.html',
        valid_referrals=valid_referrals,
        invalid_referrals=invalid_referrals,
        total_valid=len(valid_referrals),
        total_invalid=len(invalid_referrals)
    )

if __name__ == '__main__':
    app.run(debug=True)
