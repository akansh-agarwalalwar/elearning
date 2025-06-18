import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from PIL import Image
import io
from config.logging_config import log_error, log_db_operation
from exceptions.custom_exceptions import ValidationException

class FileService:
    def __init__(self):
        # Create upload directories
        self.upload_dir = Path("uploads")
        self.banner_dir = self.upload_dir / "banners"
        self.create_directories()
        
        # Allowed image formats
        self.allowed_image_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
        self.max_file_size = 5 * 1024 * 1024  # 5MB
        self.max_image_dimensions = (1920, 1080)  # Max width, height
        
    def create_directories(self):
        """Create necessary directories for file uploads"""
        self.upload_dir.mkdir(exist_ok=True)
        self.banner_dir.mkdir(exist_ok=True)
    
    async def validate_image_file(self, file: UploadFile) -> dict:
        """Validate uploaded image file"""
        errors = []
        
        # Check file type
        if file.content_type not in self.allowed_image_types:
            errors.append(f"File type not allowed. Allowed types: {', '.join(self.allowed_image_types)}")
        
        # Check file size
        if file.size and file.size > self.max_file_size:
            errors.append(f"File size too large. Maximum size: {self.max_file_size // (1024*1024)}MB")
        
        # Check file extension
        if file.filename:
            file_extension = file.filename.lower().split('.')[-1]
            allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
            if file_extension not in allowed_extensions:
                errors.append(f"File extension not allowed. Allowed extensions: {', '.join(allowed_extensions)}")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    async def process_and_save_banner_image(self, file: UploadFile, course_id: str) -> str:
        """Process and save banner image with optimization"""
        try:
            # Validate file
            validation = await self.validate_image_file(file)
            if not validation["is_valid"]:
                raise ValidationException(
                    "Image validation failed",
                    "banner_image",
                    {"errors": validation["errors"]}
                )
            
            # Read file content
            content = await file.read()
            
            # Open image with PIL for processing
            image = Image.open(io.BytesIO(content))
            
            # Resize image if too large
            if image.size[0] > self.max_image_dimensions[0] or image.size[1] > self.max_image_dimensions[1]:
                image.thumbnail(self.max_image_dimensions, Image.Resampling.LANCZOS)
            
            # Generate unique filename
            file_extension = file.filename.lower().split('.')[-1] if file.filename else 'jpg'
            filename = f"banner_{course_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
            file_path = self.banner_dir / filename
            
            # Save optimized image
            image.save(file_path, quality=85, optimize=True)
            
            # Return relative path for database storage
            relative_path = f"uploads/banners/{filename}"
            
            log_db_operation("CREATE", "banner_image", course_id, f"Saved: {filename}")
            
            return relative_path
            
        except Exception as e:
            log_error("BANNER_IMAGE_PROCESSING_FAILED", str(e), course_id)
            raise ValidationException(
                "Failed to process banner image",
                "banner_image",
                {"error": str(e)}
            )
    
    async def delete_banner_image(self, image_path: str) -> bool:
        """Delete banner image file"""
        try:
            if image_path and image_path.startswith("uploads/banners/"):
                file_path = Path(image_path)
                if file_path.exists():
                    file_path.unlink()
                    log_db_operation("DELETE", "banner_image", None, f"Deleted: {image_path}")
                    return True
            return False
        except Exception as e:
            log_error("BANNER_IMAGE_DELETE_FAILED", str(e), None, f"Path: {image_path}")
            return False
    
    async def get_banner_image_path(self, course_id: str) -> Optional[str]:
        """Get banner image path for a course"""
        try:
            # Look for existing banner images for this course
            pattern = f"banner_{course_id}_*"
            for file_path in self.banner_dir.glob(pattern):
                return f"uploads/banners/{file_path.name}"
            return None
        except Exception as e:
            log_error("BANNER_IMAGE_PATH_GET_FAILED", str(e), course_id)
            return None
    
    def get_image_url(self, image_path: str) -> str:
        """Generate public URL for image"""
        if image_path:
            return f"/static/{image_path}"
        return ""
    
# Global file service instance
file_service = FileService() 