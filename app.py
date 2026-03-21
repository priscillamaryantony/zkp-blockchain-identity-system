from flask import Flask, render_template, request, Response, jsonify
from blockchain import Blockchain, Block, hash_identity, verify_proof, is_chain_valid
from database import init_db, insert_block, get_blocks
import csv
import io
import logging
import re
import os

app = Flask(__name__)

# ✅ Create DB only if not exists
if not os.path.exists("blockchain.db"):
    init_db()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Initialize blockchain
my_blockchain = Blockchain()


# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')


# 📊 Dashboard Page
@app.route('/dashboard')
def dashboard():
    rows = get_blocks()

    blocks = []
    for row in rows:
        block = {
            "index": row[1],
            "timestamp": row[2],
            "hash": row[3],
            "previous_hash": row[4],
            "proof": row[5],
            "identity": row[6],
            "reason": row[7] if len(row) > 7 else "N/A",
            "user": row[8] if len(row) > 8 else "Unknown"
        }
        blocks.append(block)

    # Filters
    filter_type = request.args.get('filter')
    search_query = request.args.get('search', '').lower()

    if filter_type == "verified":
        blocks = [b for b in blocks if b["proof"] == "VALID_USER"]
    elif filter_type == "failed":
        blocks = [b for b in blocks if b["proof"] == "INVALID"]

    # 🔍 Search by hash + name
    if search_query:
        blocks = [
            b for b in blocks
            if search_query in b["identity"].lower()
            or search_query in b["user"].lower()
        ]

    # 📊 Metrics
    total = len(blocks)
    verified = sum(1 for b in blocks if b["proof"] == "VALID_USER")
    failed = total - verified

    success_rate = round((verified / total) * 100, 2) if total > 0 else 0

    # 🔗 Blockchain integrity
    valid = is_chain_valid(my_blockchain.chain)

    return render_template(
        'dashboard.html',
        chain=blocks[::-1],
        total=total,
        verified=verified,
        failed=failed,
        success_rate=success_rate,
        valid=valid
    )


# 🧠 NEW: KYC VALIDATION FUNCTION
def validate_kyc(id_number):
    # Aadhaar: 12 digits
    if id_number.isdigit() and len(id_number) == 12:
        return True, "Valid Aadhaar"

    # PAN: 5 letters + 4 digits + 1 letter
    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    if re.match(pan_pattern, id_number):
        return True, "Valid PAN"

    return False, "Invalid ID Format"


# 📝 Registration + Verification
@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form.get('name', '').strip()
        age = int(request.form.get('age', 0))
        id_number = request.form.get('id_number', '').strip().upper()

        # 🔒 Security
        if len(id_number) > 20:
            return "Error: ID too long"

        if not name:
            return "Error: Name is required"

        if age <= 0:
            return "Error: Invalid age"

        # 🧠 KYC VALIDATION (NEW)
        kyc_valid, kyc_message = validate_kyc(id_number)

        # 🔐 Hash identity
        hashed_user = hash_identity({
            "user": name,
            "age": age,
            "id": id_number
        })

        # 🧠 Proof + Reason
        if age < 18:
            proof = "INVALID"
            reason = "Underage"
        elif not kyc_valid:
            proof = "INVALID"
            reason = kyc_message
        else:
            proof = "VALID_USER"
            reason = kyc_message

        # 🧾 Logging
        logging.info(f"{name} → {proof} ({reason})")

        # 🔗 Create block
        new_block = Block(
            len(my_blockchain.chain),
            {
                "hash": hashed_user,
                "proof": proof,
                "reason": reason,
                "user": name
            },
            ""
        )

        my_blockchain.add_block(new_block)

        # 💾 Save to DB
        insert_block(new_block)

        # ✅ Verify proof
        result = verify_proof(proof)

        # 🔐 Chain validation
        valid = is_chain_valid(my_blockchain.chain)

        # 📊 Latest blocks
        recent_blocks = my_blockchain.chain[::-1][:5]

        return render_template(
            'result.html',
            name=name,
            result=result,
            chain=recent_blocks,
            valid=valid
        )

    except Exception as e:
        return f"Something went wrong: {str(e)}"


# 📥 Export CSV
@app.route('/export')
def export_data():
    rows = get_blocks()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Index", "Timestamp", "Hash", "Previous Hash", "Proof", "User", "Reason"])

    for row in rows:
        writer.writerow([
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[8] if len(row) > 8 else "",
            row[7] if len(row) > 7 else ""
        ])

    output.seek(0)

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=blockchain_data.csv"}
    )


# 🌐 API Endpoint
@app.route('/api/blocks')
def api_blocks():
    rows = get_blocks()

    data = []
    for row in rows:
        data.append({
            "index": row[1],
            "timestamp": row[2],
            "hash": row[3],
            "previous_hash": row[4],
            "proof": row[5],
            "identity": row[6],
            "reason": row[7] if len(row) > 7 else "",
            "user": row[8] if len(row) > 8 else ""
        })

    return jsonify(data)


# ▶ Run App
if __name__ == '__main__':
    app.run(debug=False)