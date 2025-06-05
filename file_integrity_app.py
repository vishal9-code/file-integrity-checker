import streamlit as st
import os
import hashlib
import json
from pathlib import Path

# ---------- Core Functions ----------
def get_file_hash(file):
    hash_algo = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_algo.update(chunk)
    file.seek(0)
    return hash_algo.hexdigest()

def save_hashes_from_files(uploaded_files):
    hashes = {}
    for uploaded_file in uploaded_files:
        file_hash = get_file_hash(uploaded_file)
        hashes[uploaded_file.name] = file_hash
    with open("uploaded_hashes.json", "w") as f:
        json.dump(hashes, f, indent=4)
    return hashes

def check_uploaded_files(uploaded_files):
    if not os.path.exists("uploaded_hashes.json"):
        return "❌ No saved hash file found.", []

    with open("uploaded_hashes.json", "r") as f:
        old_hashes = json.load(f)

    changed_files = []
    for uploaded_file in uploaded_files:
        current_hash = get_file_hash(uploaded_file)
        saved_hash = old_hashes.get(uploaded_file.name)
        if saved_hash and saved_hash != current_hash:
            changed_files.append(uploaded_file.name)

    if changed_files:
        return "⚠️ Some files were changed:", changed_files
    return "✅ All uploaded files are intact.", []

# ---------- Streamlit UI ----------
st.set_page_config(page_title="🔐 File Integrity Checker", layout="centered")
st.title("🛡️ File Integrity Checker with Upload")

uploaded_files = st.file_uploader("Upload files to check:", accept_multiple_files=True)

if uploaded_files:
    if st.button("💾 Save Hashes"):
        save_hashes_from_files(uploaded_files)
        st.success("✅ Hashes saved successfully.")

    if st.button("🔍 Check File Integrity"):
        result, changed_files = check_uploaded_files(uploaded_files)
        if changed_files:
            st.warning(result)
            for f in changed_files:
                st.code(f)
        else:
            st.success(result)
