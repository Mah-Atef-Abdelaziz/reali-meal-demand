"""Employees Router — CRUD and analytics for employees."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from models import Employee, Department, WorkLocation
from schemas import EmployeeResponse, EmployeeListResponse
from auth import get_current_user_id

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=EmployeeListResponse)
async def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    department_id: Optional[int] = None,
    location_id: Optional[int] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = True,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    query = select(Employee)
    count_query = select(func.count(Employee.id))

    if department_id:
        query = query.where(Employee.department_id == department_id)
        count_query = count_query.where(Employee.department_id == department_id)
    if location_id:
        query = query.where(Employee.work_location_id == location_id)
        count_query = count_query.where(Employee.work_location_id == location_id)
    if is_active is not None:
        query = query.where(Employee.is_active == is_active)
        count_query = count_query.where(Employee.is_active == is_active)
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (Employee.first_name.ilike(search_filter)) |
            (Employee.last_name.ilike(search_filter)) |
            (Employee.employee_number.ilike(search_filter))
        )
        count_query = count_query.where(
            (Employee.first_name.ilike(search_filter)) |
            (Employee.last_name.ilike(search_filter)) |
            (Employee.employee_number.ilike(search_filter))
        )

    total = (await db.execute(count_query)).scalar() or 0
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Employee.id)
    result = await db.execute(query)
    employees = result.scalars().all()

    return EmployeeListResponse(
        items=[EmployeeResponse.model_validate(e) for e in employees],
        total=total, page=page, page_size=page_size
    )


@router.get("/stats")
async def employee_stats(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    total = (await db.execute(select(func.count(Employee.id)))).scalar() or 0
    active = (await db.execute(
        select(func.count(Employee.id)).where(Employee.is_active == True))).scalar() or 0

    dept_result = await db.execute(
        select(Department.name, func.count(Employee.id).label("count"))
        .join(Employee, Employee.department_id == Department.id)
        .where(Employee.is_active == True)
        .group_by(Department.name)
        .order_by(func.count(Employee.id).desc())
    )
    by_dept = [{"name": r.name, "count": r.count} for r in dept_result.all()]

    loc_result = await db.execute(
        select(WorkLocation.name, WorkLocation.location_type,
               func.count(Employee.id).label("count"))
        .join(Employee, Employee.work_location_id == WorkLocation.id)
        .where(Employee.is_active == True)
        .group_by(WorkLocation.name, WorkLocation.location_type)
        .order_by(func.count(Employee.id).desc())
    )
    by_loc = [{"name": r.name, "type": r.location_type, "count": r.count}
              for r in loc_result.all()]

    return {"total": total, "active": active, "inactive": total - active,
            "by_department": by_dept, "by_location": by_loc}


@router.get("/departments")
async def list_departments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).order_by(Department.name))
    return [{"id": d.id, "name": d.name, "code": d.code} for d in result.scalars().all()]


@router.get("/locations")
async def list_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(WorkLocation).order_by(WorkLocation.name))
    return [{"id": l.id, "name": l.name, "code": l.code, "type": l.location_type,
             "city": l.city, "capacity": l.capacity} for l in result.scalars().all()]
