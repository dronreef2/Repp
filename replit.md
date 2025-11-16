# Overview

This is an AI-powered Educational Assistant SaaS application built as a microservice using Flask and Python. The system provides intelligent learning assistance through natural language interactions, storing user query history and generating personalized educational responses using Google's Gemini AI. The application features automated progress reporting, rate limiting for security, and dynamic content personalization based on user expertise levels.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture

**Framework**: Flask-based REST API microservice
- **Language**: Python
- **Web Framework**: Flask for HTTP request handling and routing
- **Rationale**: Flask provides lightweight, flexible foundation for rapid prototyping while maintaining production readiness

## Data Storage

**Primary Database**: ReplitDB (key-value store)
- **Schema Design**: Prefix-based indexing using pattern `query:{user_id}:{timestamp}`
- **Rationale**: ReplitDB offers zero-configuration persistence suitable for MVP deployment on Replit infrastructure
- **Query Pattern**: Prefix matching enables efficient user-specific history retrieval
- **Data Structure**: Stores user queries with temporal ordering for chronological analysis

## API Design

**RESTful Endpoints**:
1. `GET /` - Health check and version info
2. `POST /api/ask` - Primary query endpoint with AI response generation
3. `GET /api/get_history` - User query history retrieval
4. `GET /api/report` - Automated progress analytics

**Request/Response Pattern**:
- Strict JSON schema enforcement for predictable data contracts
- Comprehensive error handling (400 for validation, 429 for rate limits)
- User identification via `user_id` parameter for session tracking

## AI Integration

**Provider**: Google Gemini API
- **Integration Pattern**: Direct API calls via `integrar_gemini()` function
- **Prompt Engineering**: System prompts define assistant role and output constraints
- **Response Format**: Enforced JSON schema `{"summary": "string", "next_steps": ["string", "string", "string"]}`
- **Rationale**: Gemini provides cost-effective, high-quality generative responses with structured output capabilities

**Personalization Layer**:
- Dynamic system prompts based on user `level` parameter (básico, universitário, etc.)
- Context-aware response generation adapting tone and depth to user expertise

## Security & Performance

**API Key Management**:
- Environment variable `GEMINI_API_KEY` stored in `.env` file
- Rationale: Prevents credential exposure in version control

**Rate Limiting**:
- 5 requests per minute per `user_id` on `POST /api/ask`
- Implementation: Flask-Limiter or custom ReplitDB counter logic
- Rationale: Prevents abuse and manages AI API costs

**Error Handling**:
- Input validation at endpoint level
- Graceful degradation with appropriate HTTP status codes
- Malformed JSON and missing field detection

## Analytics & Automation

**Progress Reporting Agent**:
- Function: `gerar_relatorio_analitico()` analyzes user query patterns
- Uses Gemini to generate insights on learning diversity and focus areas
- Output schema: `{"analysis_summary": "string", "focus_areas": ["array"], "recommendation": "string"}`
- Rationale: Automated coaching feedback without manual intervention

# External Dependencies

## Third-Party APIs
- **Google Gemini API**: Generative AI for educational content and analysis
  - Authentication: API key-based
  - Rate limits: Managed at application layer

## Python Libraries
- **Flask**: Web framework for REST API
- **requests**: HTTP client for Gemini API integration (or native Gemini SDK)
- **replit**: ReplitDB client for data persistence
- **Flask-Limiter** (or equivalent): Rate limiting middleware

## Infrastructure
- **Replit Platform**: Hosting environment
- **ReplitDB**: Managed key-value database service
- **Environment Variables**: `.env` file for configuration management

## Version Control
- **GitHub Repository**: `https://github.com/dronreef2/Repp.git`
- Deployment workflow: Direct git push from Replit environment