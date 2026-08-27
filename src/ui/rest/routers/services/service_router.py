from fastapi import APIRouter, Depends
from src.ports.driver.for_manage_services.dto.service_dto import ServiceDTO, ServiceCreateDTO, ServiceUpdateDTO
from src.domain.services.application.service_use_cases import ServiceUseCases
from src.ui.rest.dependencies import require_admin_token


service_router = APIRouter(
    prefix="/services",
    tags=["services"],
    dependencies=[Depends(require_admin_token)],
)

@service_router.post("/", response_model=ServiceDTO)
def create_service(service: ServiceCreateDTO, use_case: ServiceUseCases = Depends(get_service_use_cases)):
    return use_case.create_service(service)

@service_router.put("/{service_id}", response_model=ServiceDTO)
def update_service(service_id: int, service: ServiceUpdateDTO, use_case: ServiceUseCases = Depends(get_service_use_cases)) -> ServiceDTO:
    return use_case.update_service(service_id, service)

@service_router.delete("/{service_id}", response_model=ServiceDTO)
def delete_service(service_id: int, use_case: ServiceUseCases = Depends(get_service_use_cases)) -> ServiceDTO:
    return use_case.delete_service(service_id)

@service_router.get("/{service_id}", response_model=ServiceDTO)
def get_service(service_id: int, use_case: ServiceUseCases = Depends(get_service_use_cases)) -> ServiceDTO:
    return use_case.get_service(service_id)