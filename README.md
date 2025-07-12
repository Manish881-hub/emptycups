# EmptyCup Portfolio

EmptyCup Portfolio is a web application that helps users discover and manage design studios. It features a clean, modern interface for browsing design studios, with capabilities to view details, shortlist favorites, and manage listings.

## Features

- 📋 Browse design studio listings
- 💾 Shortlist favorite studios
- 🖼️ Multiple view options (List, Gallery, Map)
- ⭐ Studio ratings and reviews
- 📊 Studio statistics (projects, experience, pricing)
- 📱 Responsive design for all devices

## Tech Stack

### Backend
- Python Flask server
- RESTful API architecture
- JSON-based data storage
- CORS enabled for frontend integration
- Docker support

### Frontend
- HTML5
- CSS3
- JavaScript
- Modern UI with Inter font family
- Responsive design

## Project Structure

```
emptycups/
  ├── backend/
  │   ├── app.py           # Flask application
  │   ├── data/
  │   │   └── listings.json # Data storage
  │   ├── Dockerfile       # Docker configuration
  │   └── requirement.txt  # Python dependencies
  └── frontend/
      ├── index.html      # Main HTML file
      ├── scripts/
      │   └── app.js      # Frontend JavaScript
      └── styles/
          └── main.css    # CSS styles
```

## API Endpoints

- `GET /api/health` - Health check endpoint
- `GET /api/listings` - Get all listings
- `GET /api/listings/<listing_id>` - Get specific listing
- `POST /api/listings` - Create new listing
- `GET /api/shortlist` - Get shortlisted items
- `POST /api/shortlist/<listing_id>` - Add to shortlist
- `DELETE /api/shortlist/<listing_id>` - Remove from shortlist
- `POST /api/shortlist/<listing_id>/toggle` - Toggle shortlist status

## Setup and Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirement.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

The server will start on port 5000 by default.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Serve the frontend files using any static file server of your choice.

### Docker Setup

The backend includes Docker support. To run using Docker:

```bash
cd backend
docker build -t emptycup-backend .
docker run -p 5000:5000 emptycup-backend
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
