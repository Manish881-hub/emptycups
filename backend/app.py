from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Configuration
DATA_FILE = 'data/listings.json'
PORT = int(os.environ.get('PORT', 5000))

# Utility functions
def load_listings():
    """Load listings from JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # Ensure shortlisted array exists
            if 'shortlisted' not in data:
                data['shortlisted'] = []
            return data
    except FileNotFoundError:
        return {"listings": [], "shortlisted": []}
    except json.JSONDecodeError:
        return {"listings": [], "shortlisted": []}

def save_listings(data):
    """Save listings to JSON file"""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "EmptyCup Portfolio API"
    })

@app.route('/api/listings', methods=['GET'])
def get_listings():
    """Get all listings"""
    try:
        data = load_listings()
        return jsonify({
            "success": True,
            "data": data['listings'],
            "count": len(data['listings'])
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    """Get a specific listing by ID"""
    try:
        data = load_listings()
        listing = next((l for l in data['listings'] if l['id'] == listing_id), None)

        if not listing:
            return jsonify({
                "success": False,
                "error": "Listing not found"
            }), 404

        return jsonify({
            "success": True,
            "data": listing
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/shortlist', methods=['GET'])
def get_shortlisted():
    """Get all shortlisted listings"""
    try:
        data = load_listings()
        shortlisted_ids = data.get('shortlisted', [])
        print(f"Getting shortlisted items. IDs: {shortlisted_ids}")

        shortlisted_listings = [
            listing for listing in data['listings']
            if listing['id'] in shortlisted_ids
        ]
        print(f"Found {len(shortlisted_listings)} shortlisted listings")

        return jsonify({
            "success": True,
            "data": shortlisted_listings,
            "count": len(shortlisted_listings)
        })
    except Exception as e:
        print(f"Error getting shortlisted items: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/shortlist/<listing_id>', methods=['POST'])
def add_to_shortlist(listing_id):
    """Add a listing to shortlist"""
    try:
        data = load_listings()
        print(f"Adding {listing_id} to shortlist")

        # Check if listing exists
        listing = next((l for l in data['listings'] if l['id'] == listing_id), None)
        if not listing:
            print(f"Listing {listing_id} not found")
            return jsonify({
                "success": False,
                "error": "Listing not found"
            }), 404

        # Initialize shortlisted array if it doesn't exist
        if 'shortlisted' not in data:
            data['shortlisted'] = []

        # Add to shortlist if not already there
        if listing_id not in data['shortlisted']:
            data['shortlisted'].append(listing_id)
            print(f"Added {listing_id} to shortlist. Current shortlist: {data['shortlisted']}")

            if save_listings(data):
                return jsonify({
                    "success": True,
                    "message": "Added to shortlist",
                    "listing_id": listing_id
                })
            else:
                print("Failed to save data")
                return jsonify({
                    "success": False,
                    "error": "Failed to save data"
                }), 500
        else:
            print(f"{listing_id} already in shortlist")
            return jsonify({
                "success": True,
                "message": "Already in shortlist",
                "listing_id": listing_id
            })

    except Exception as e:
        print(f"Error adding to shortlist: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/shortlist/<listing_id>', methods=['DELETE'])
def remove_from_shortlist(listing_id):
    """Remove a listing from shortlist"""
    try:
        data = load_listings()

        if 'shortlisted' not in data:
            data['shortlisted'] = []

        # Remove from shortlist if present
        if listing_id in data['shortlisted']:
            data['shortlisted'].remove(listing_id)

            if save_listings(data):
                return jsonify({
                    "success": True,
                    "message": "Removed from shortlist",
                    "listing_id": listing_id
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "Failed to save data"
                }), 500
        else:
            return jsonify({
                "success": True,
                "message": "Not in shortlist",
                "listing_id": listing_id
            })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/shortlist/<listing_id>/toggle', methods=['POST'])
def toggle_shortlist(listing_id):
    """Toggle a listing in shortlist (add if not present, remove if present)"""
    try:
        data = load_listings()

        # Check if listing exists
        listing = next((l for l in data['listings'] if l['id'] == listing_id), None)
        if not listing:
            return jsonify({
                "success": False,
                "error": "Listing not found"
            }), 404

        if 'shortlisted' not in data:
            data['shortlisted'] = []

        # Toggle shortlist status
        if listing_id in data['shortlisted']:
            data['shortlisted'].remove(listing_id)
            action = "removed"
            is_shortlisted = False
        else:
            data['shortlisted'].append(listing_id)
            action = "added"
            is_shortlisted = True

        if save_listings(data):
            return jsonify({
                "success": True,
                "message": f"Listing {action}",
                "listing_id": listing_id,
                "is_shortlisted": is_shortlisted
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save data"
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/listings', methods=['POST'])
def create_listing():
    """Create a new listing (for admin use)"""
    try:
        listing_data = request.get_json()

        if not listing_data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400

        # Validate required fields
        required_fields = ['name', 'description', 'projects', 'years', 'price', 'phones']
        for field in required_fields:
            if field not in listing_data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400

        data = load_listings()

        # Create new listing with generated ID
        new_listing = {
            "id": str(uuid.uuid4()),
            "name": listing_data['name'],
            "rating": listing_data.get('rating', 4.0),
            "description": listing_data['description'],
            "projects": listing_data['projects'],
            "years": listing_data['years'],
            "price": listing_data['price'],
            "phones": listing_data['phones'],
            "created_at": datetime.now().isoformat()
        }

        data['listings'].append(new_listing)

        if save_listings(data):
            return jsonify({
                "success": True,
                "message": "Listing created successfully",
                "data": new_listing
            }), 201
        else:
            return jsonify({
                "success": False,
                "error": "Failed to save listing"
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    print(f"🚀 EmptyCup Portfolio API starting on port {PORT}")
    print(f"📁 Data file: {DATA_FILE}")
    print(f"🌐 Health check: http://localhost:{PORT}/api/health")
    app.run(host='0.0.0.0', port=PORT, debug=True)