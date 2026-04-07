#!/bin/bash

echo "🚀 Setting up NBFC Cross-sell MVP..."
echo ""

# Create virtual environment
echo "1️⃣ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "2️⃣ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "3️⃣ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Generate data
echo "4️⃣ Generating synthetic NBFC customer data..."
python generate_data.py

# Train model
echo "5️⃣ Training propensity model..."
python train_model.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To launch the dashboard, run:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
