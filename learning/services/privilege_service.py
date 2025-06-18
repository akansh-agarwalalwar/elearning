from sqlalchemy.orm import Session
from database.models import User, Privilege
from utils.enums import PrivilegeName, UserRole
from typing import List, Optional
from datetime import datetime

class PrivilegeService:
    def __init__(self, db: Session):
        self.db = db
    
    def assign_privilege_to_instructor(
        self, 
        instructor_id: int, 
        privilege_name: str, 
        privilege_description: str = None, 
        admin_id: int = None
    ) -> Privilege:
        """
        Assign a privilege to an instructor by an admin
        """
        # Validate privilege name
        try:
            PrivilegeName(privilege_name)
        except ValueError:
            raise ValueError(f"Invalid privilege name: {privilege_name}")
        
        # Verify the instructor exists and has instructor role
        instructor = self.db.query(User).filter(
            User.id == instructor_id,
            User.role == UserRole.INSTRUCTOR,
            User.is_active == True
        ).first()
        
        if not instructor:
            raise ValueError("Instructor not found or invalid")
        
        # Verify the admin exists and has admin role
        admin = self.db.query(User).filter(
            User.id == admin_id,
            User.role == UserRole.ADMIN,
            User.is_active == True
        ).first()
        
        if not admin:
            raise ValueError("Admin not found or invalid")
        
        # Check if privilege already exists for this instructor
        existing_privilege = self.db.query(Privilege).filter(
            Privilege.instructor_id == instructor_id,
            Privilege.privilege_name == privilege_name,
            Privilege.is_active == True
        ).first()
        
        if existing_privilege:
            raise ValueError(f"Privilege '{privilege_name}' already assigned to this instructor")
        
        # Use enum description if none provided
        if not privilege_description:
            privilege_description = PrivilegeName.get_privilege_description(privilege_name)
        
        # Create new privilege
        privilege = Privilege(
            instructor_id=instructor_id,
            privilege_name=privilege_name,
            privilege_description=privilege_description,
            assigned_by=admin_id,
            assigned_at=datetime.utcnow()
        )
        
        self.db.add(privilege)
        self.db.commit()
        self.db.refresh(privilege)
        
        return privilege
    
    def assign_default_privileges_to_instructor(self, instructor_id: int, admin_id: int) -> List[Privilege]:
        """
        Assign default privileges to a new instructor
        """
        default_privileges = PrivilegeName.get_default_instructor_privileges()
        assigned_privileges = []
        
        for privilege_name in default_privileges:
            try:
                privilege = self.assign_privilege_to_instructor(
                    instructor_id=instructor_id,
                    privilege_name=privilege_name,
                    admin_id=admin_id
                )
                assigned_privileges.append(privilege)
            except ValueError as e:
                # Skip if privilege already exists
                if "already assigned" not in str(e):
                    raise e
        
        return assigned_privileges
    
    def revoke_privilege_from_instructor(
        self, 
        instructor_id: int, 
        privilege_name: str, 
        admin_id: int
    ) -> bool:
        """
        Revoke a privilege from an instructor by an admin
        """
        # Validate privilege name
        try:
            PrivilegeName(privilege_name)
        except ValueError:
            raise ValueError(f"Invalid privilege name: {privilege_name}")
        
        # Verify the admin exists and has admin role
        admin = self.db.query(User).filter(
            User.id == admin_id,
            User.role == UserRole.ADMIN,
            User.is_active == True
        ).first()
        
        if not admin:
            raise ValueError("Admin not found or invalid")
        
        # Find and deactivate the privilege
        privilege = self.db.query(Privilege).filter(
            Privilege.instructor_id == instructor_id,
            Privilege.privilege_name == privilege_name,
            Privilege.is_active == True
        ).first()
        
        if not privilege:
            raise ValueError(f"Privilege '{privilege_name}' not found for this instructor")
        
        privilege.is_active = False
        self.db.commit()
        
        return True
    
    def get_instructor_privileges(self, instructor_id: int) -> List[Privilege]:
        """
        Get all active privileges for an instructor
        """
        privileges = self.db.query(Privilege).filter(
            Privilege.instructor_id == instructor_id,
            Privilege.is_active == True
        ).all()
        
        return privileges
    
    def check_instructor_privilege(self, instructor_id: int, privilege_name: str) -> bool:
        """
        Check if an instructor has a specific privilege
        """
        # Validate privilege name
        try:
            PrivilegeName(privilege_name)
        except ValueError:
            return False
        
        privilege = self.db.query(Privilege).filter(
            Privilege.instructor_id == instructor_id,
            Privilege.privilege_name == privilege_name,
            Privilege.is_active == True
        ).first()
        
        return privilege is not None
    
    def get_all_privileges(self) -> List[Privilege]:
        """
        Get all privileges (for admin dashboard)
        """
        privileges = self.db.query(Privilege).filter(
            Privilege.is_active == True
        ).all()
        
        return privileges
    
    def get_privileges_by_admin(self, admin_id: int) -> List[Privilege]:
        """
        Get all privileges assigned by a specific admin
        """
        privileges = self.db.query(Privilege).filter(
            Privilege.assigned_by == admin_id,
            Privilege.is_active == True
        ).all()
        
        return privileges
    
    def get_available_privileges(self) -> List[dict]:
        """
        Get all available privilege names with descriptions
        """
        privileges = []
        for privilege in PrivilegeName:
            privileges.append({
                "name": privilege.value,
                "description": PrivilegeName.get_privilege_description(privilege.value)
            })
        return privileges
    
    def bulk_assign_privileges(
        self, 
        instructor_id: int, 
        privilege_names: List[str], 
        admin_id: int
    ) -> List[Privilege]:
        """
        Assign multiple privileges to an instructor at once
        """
        assigned_privileges = []
        
        for privilege_name in privilege_names:
            try:
                privilege = self.assign_privilege_to_instructor(
                    instructor_id=instructor_id,
                    privilege_name=privilege_name,
                    admin_id=admin_id
                )
                assigned_privileges.append(privilege)
            except ValueError as e:
                # Skip if privilege already exists
                if "already assigned" not in str(e):
                    raise e
        
        return assigned_privileges
    
    def bulk_revoke_privileges(
        self, 
        instructor_id: int, 
        privilege_names: List[str], 
        admin_id: int
    ) -> List[str]:
        """
        Revoke multiple privileges from an instructor at once
        """
        revoked_privileges = []
        
        for privilege_name in privilege_names:
            try:
                self.revoke_privilege_from_instructor(
                    instructor_id=instructor_id,
                    privilege_name=privilege_name,
                    admin_id=admin_id
                )
                revoked_privileges.append(privilege_name)
            except ValueError as e:
                # Skip if privilege doesn't exist
                if "not found" not in str(e):
                    raise e
        
        return revoked_privileges 