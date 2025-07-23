from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Claim(Base):
    __tablename__ = "claims"
    claim_id = Column(String, primary_key=True, index=True)
    provider_id = Column(String, ForeignKey("providers.provider_id"), index=True)
    risk_id = Column(String, ForeignKey("risk_ratings.risk_id"), index=True)
    policy_id = Column(String, ForeignKey("insurance_policies.policy_id"), index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"), index=True)
    status = Column(String)
    submission_date = Column(String)
    summary = Column(Text)
    ex_gratia_flag = Column(Boolean)
    appeal_case_flag = Column(Boolean)
    reason_code = Column(String)
    reason_description = Column(Text)
    last_status_update_date = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    
    # Relationships for easier data access
    provider = relationship("Provider", back_populates="claims")
    risk_rating = relationship("RiskRating", back_populates="claims")
    insurance_policy = relationship("InsurancePolicy", back_populates="claims")
    patient = relationship("Patient", back_populates="claims")
    claim_riders = relationship("ClaimClaimRider", back_populates="claim")

class Provider(Base):
    __tablename__ = "providers"
    provider_id = Column(String, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    location = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    
    # Relationships
    claims = relationship("Claim", back_populates="provider")

class RiskRating(Base):
    __tablename__ = "risk_ratings"
    risk_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(String)
    updated_at = Column(String)
    
    # Relationships
    claims = relationship("Claim", back_populates="risk_rating")

class ClaimRider(Base):
    __tablename__ = "claim_riders"
    rider_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(String)
    updated_at = Column(String)
    
    # Relationships
    claim_associations = relationship("ClaimClaimRider", back_populates="rider")

class ClaimClaimRider(Base):
    __tablename__ = "claim_claim_riders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(String, ForeignKey("claims.claim_id"), index=True)
    rider_id = Column(String, ForeignKey("claim_riders.rider_id"), index=True)
    selected_status = Column(Boolean)
    created_at = Column(String)
    
    # Relationships
    claim = relationship("Claim", back_populates="claim_riders")
    rider = relationship("ClaimRider", back_populates="claim_associations")

class InsurancePolicy(Base):
    __tablename__ = "insurance_policies"
    policy_id = Column(String, primary_key=True, index=True)
    policy_number = Column(String, unique=True, index=True)
    policy_name = Column(String)
    policy_type = Column(String)  # Individual, Family, Group
    coverage_amount = Column(String)  # Using String for now to maintain compatibility
    annual_premium = Column(String)  # Using String for now to maintain compatibility
    deductible_amount = Column(String)  # Using String for now to maintain compatibility
    copay_percentage = Column(String)  # Using String for now to maintain compatibility
    coverage_description = Column(Text)
    start_date = Column(String)
    end_date = Column(String)
    status = Column(String)  # Active, Expired, Suspended
    created_at = Column(String)
    updated_at = Column(String)
    
    # Relationships
    claims = relationship("Claim", back_populates="insurance_policy")
    patients = relationship("Patient", back_populates="policy")

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(String, primary_key=True, index=True)
    policy_id = Column(String, ForeignKey("insurance_policies.policy_id"), index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)  # Using String for now to maintain compatibility
    gender = Column(String)
    phone_number = Column(String)
    email = Column(String)
    address = Column(Text)
    relationship_to_policy_holder = Column(String)  # Self, Spouse, Child, Dependent
    created_at = Column(String)
    updated_at = Column(String)
    
    # Relationships
    policy = relationship("InsurancePolicy", back_populates="patients")
    claims = relationship("Claim", back_populates="patient")