"""
Configuration settings for Medical Chatbot Application
"""
import os
from typing import Optional


class Settings:
    """Application configuration settings"""
    
    # Application Settings
    APP_HOST: str = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT: int = int(os.getenv('APP_PORT', '5001'))
    APP_NAME: str = "Medical Chatbot API"
    
    # ChromaDB Configuration
    CHROMA_HOST: str = os.getenv('CHROMA_HOST', '127.0.0.1')
    CHROMA_PORT: int = int(os.getenv('CHROMA_PORT', '8000'))
    
    # Ollama Configuration (local LLM)
    OLLAMA_HOST: str = os.getenv('OLLAMA_HOST', '127.0.0.1')
    OLLAMA_PORT: int = int(os.getenv('OLLAMA_PORT', '11434'))
    
    # MongoDB Configuration
    MONGO_USERNAME: str = os.getenv('MONGO_USERNAME', 'krishana85289')
    MONGO_PASSWORD: str = os.getenv('MONGO_PASSWORD', 'Kkkk@85289')
    MONGO_CLUSTER: str = os.getenv('MONGO_CLUSTER', 'cluster0.ddvpueb.mongodb.net')
    MONGO_DBNAME: str = os.getenv('MONGO_DBNAME', 'cosmosAI')
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    
    # File Upload Settings
    UPLOAD_DIR: str = os.getenv('UPLOAD_DIR', 'uploaded_pdfs')
    EXCEL_DIR: str = os.getenv('EXCEL_DIR', 'Excel_files')
    COMBINED_PDF: str = os.getenv('COMBINED_PDF', 'combined.pdf')
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    @classmethod
    def get_mongo_uri(cls) -> str:
        """Generate MongoDB connection URI"""
        from urllib.parse import quote_plus
        username = quote_plus(cls.MONGO_USERNAME)
        password = quote_plus(cls.MONGO_PASSWORD)
        return f"mongodb+srv://{username}:{password}@{cls.MONGO_CLUSTER}/{cls.MONGO_DBNAME}?retryWrites=true&w=majority"


# Global settings instance
settings = Settings()

