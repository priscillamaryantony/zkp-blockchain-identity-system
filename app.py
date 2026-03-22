from flask import Flask, render_template, request, Response, jsonify, redirect, url_for
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


# 🔥 LOAD BLOCKCHAIN FROM DB (Persistence Fix)
def load_chain_from_db():
    rows = get_blocks()
    chain = []

    for row in rows:
        block = Block(
            row[1],  # index
            {
                "hash": row[6],
                "proof": row[5],
                "reason": row[7] if len(row) > 7 else "",
                "user": row[8] if len(row) > 8 else ""
            },
            row[4]  # previous_hash
        )

        block.hash = row[3]
        block.timestamp = row[2]

        chain.append(block)

    return chain


# 🔥 Sync DB → Blockchain
db_chain = load_chain_from_db()
if db_chain:
    my_blockchain.chain = db_chain


# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')


# 🔐 Login Page
@app.route('/login')
def login():
    return render_template('login.html')


# 🔓 Logout
@app.route('/logout')
def logout():
    return redirect(url_for('home'))


# 📊 Dashboard Page
@app.route('/dashboard')
def dashboard():
    rows = get_blocks()

    blocks = []
    for row in rows:
        block = {
            "index": row[1],  # ✅ keep original index
            "timestamp": row[2],
            "hash": row[3],
            "previous_hash": row[4],
            "proof": row[5],
            "identity": row[6],
            "reason": row[7] if len(row) > 7 else "N/A",
            "user": row[8] if len(row) > 8 else "Unknown"
        }
        blocks.append(block)

    # Sort latest first
    blocks = sorted(blocks, key=lambda x: x["index"], reverse=True)

    # Filters
    filter_type = request.args.get('filter')
    search_query = request.args.get('search', '').strip().lower()

    filtered_blocks = blocks

    if filter_type == "verified":
        filtered_blocks = [b for b in blocks if b["proof"] == "VALID_USER"]

    elif filter_type == "failed":
        filtered_blocks = [b for b in blocks if b["proof"] == "INVALID"]

    # Search
    if search_query:
        filtered_blocks = [
            b for b in filtered_blocks
            if search_query in b["identity"].lower()
            or search_query in b["user"].lower()
        ]

    # Metrics
    total = len(filtered_blocks)
    verified = sum(1 for b in filtered_blocks if b["proof"] == "VALID_USER")
    failed = total - verified

    success_rate = round((verified / total) * 100, 2) if total > 0 else 0

    # Blockchain integrity
    valid = is_chain_valid(my_blockchain.chain)

    return render_template(
        'dashboard.html',
        chain=filtered_blocks,
        total=total,
        verified=verified,
        failed=failed,
        success_rate=success_rate,
        valid=valid
    )


# 🧠 KYC VALIDATION FUNCTION
def validate_kyc(id_number):
    if id_number.isdigit() and len(id_number) == 12:
        return True, "Valid Aadhaar"

    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    if re.match(pan_pattern, id_number):
        return True, "Valid PAN"

    return False, "Invalid ID Format"


# 📝 Registration + Verification
@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form.get('name', '').strip()
        age = int(request.form.get('age') or 0)
        id_number = request.form.get('id_number', '').strip().upper()

        if len(id_number) > 20:
            return "Error: ID too long"

        if not name:
            return "Error: Name is required"

        if age <= 0:
            return "Error: Invalid age"

        # KYC validation
        kyc_valid, kyc_message = validate_kyc(id_number)

        # Hash identity
        hashed_user = hash_identity({
            "user": name,
            "age": age,
            "id": id_number
        })

        # Proof logic
        if age < 18:
            proof = "INVALID"
            reason = "Underage"
        elif not kyc_valid:
            proof = "INVALID"
            reason = kyc_message
        else:
            proof = "VALID_USER"
            reason = kyc_message

        logging.info(f"[REGISTER] {name} → {proof} ({reason})")

        # ✅ Correct blockchain index
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

        # Save to DB
        insert_block(new_block)

        # Verify proof
        result = verify_proof(proof)

        # Validate chain
        valid = is_chain_valid(my_blockchain.chain)

        # Latest blocks
        recent_blocks = my_blockchain.chain[::-1][:5]

        # ✅ Ensure Genesis always included
        if my_blockchain.chain and my_blockchain.chain[0] not in recent_blocks:
            recent_blocks.append(my_blockchain.chain[0])

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