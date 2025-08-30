

# **Joins Note**

## **1. The Golden Rule**
- A `join()` needs a **path** from the primary entity to the target entity.
- This path is defined by a `ForeignKey` and often a `relationship()`.

## **2. The Explicit, Production-Grade Syntax**
**Always use this for clarity and control:**
```python
result = session.query(Table1, Table2).join(
    TargetTable,  # The table you are joining TO
    Table1.foreign_key == TargetTable.id  # The explicit condition
).all()
```

## **3. The Four Join Types (Explicit)**

### **INNER JOIN** (Only matches)
```python
# Employees WITH Departments
result = session.query(Employee, Department).join(
    Department, Employee.department_id == Department.id
).all()
```

### **LEFT OUTER JOIN** (All left rows + matches)
```python
# ALL Employees + their Dept (if exists)
result = session.query(Employee, Department).outerjoin(
    Department, Employee.department_id == Department.id
).all()
```

### **RIGHT OUTER JOIN** (All right rows + matches)
```python
# ALL Departments + their Employees (if exist)
result = session.query(Department, Employee).outerjoin(
    Employee, Department.id == Employee.department_id
).all()
```

### **FULL OUTER JOIN** (All rows from both tables)
```python
# Combine LEFT and RIGHT joins with UNION
left = session.query(Employee, Department).outerjoin(...)
right = session.query(Employee, Department).outerjoin(...)
result = left.union(right).all()
```

## **4. Anti-Joins (Find non-matches)**

### **Find orphans on the "Many" side**
```python
# Employees with NO Department
result = session.query(Employee).outerjoin(
    Department, Employee.department_id == Department.id
).filter(Department.id == None).all()
```

### **Find orphans on the "One" side**
```python
# Departments with NO Employees
result = session.query(Department).outerjoin(
    Employee, Department.id == Employee.department_id
).filter(Employee.id == None).all()
```

## **5. Pro Tips**
- **`isouter=True`** in `.join()` is the same as `.outerjoin()`.
- The order in `query(A, B)` determines the order of result tuples `(A_obj, B_obj)`.
- Use `func.count()` and `group_by()` for aggregations, not `len(relationship)`.
- For complex queries, **always write the explicit `ON` condition**.

## **When you forget, remember this one query:**
```python
# The template for any explicit join
result = session.query(A, B).join(
    B,  # Join TO B
    A.some_fk == B.id  # ON condition
).filter(...).all()
```
---
## **6. Explicit `ON` Clause Examples**
**Always specify the condition for clarity.**
```python
# INNER JOIN with explicit ON
result = session.query(Employee, Department).join(
    Department,  # Join TO this table
    Employee.department_id == Department.id  # ON condition
).all()

# LEFT JOIN with explicit ON
result = session.query(Employee, Department).outerjoin(
    Department,
    Employee.department_id == Department.id
).all()
```

## **7. `UNION` Example (For FULL OUTER JOIN)**
**Combine results from two queries.**
```python
# Get all Employees (left join)
q1 = session.query(Employee, Department).outerjoin(
    Department, Employee.department_id == Department.id
)
# Get all Departments (right join)
q2 = session.query(Employee, Department).outerjoin(
    Employee, Department.id == Employee.department_id
)
# Combine both for FULL OUTER effect
full_outer = q1.union(q2).all()
```

## **8. `func.count()` & `group_by()` Examples**
**Count related records using aggregation.**
```python
from sqlalchemy import func

# Count employees in each department
result = (session.query(Department.name, func.count(Employee.id))
          .join(Employee, Department.id == Employee.department_id, isouter=True)
          .group_by(Department.name)  # Essential for aggregation
          .order_by(func.count(Employee.id).desc())
          .all()
)
# Output: [('Engineering', 2), ('Marketing', 1), ('HR', 0)]

# Count departments each employee is in (silly example, demonstrates concept)
result = (session.query(Employee.name, func.count(Department.id))
          .join(Department, Employee.department_id == Department.id, isouter=True)
          .group_by(Employee.name)
          .all()
)
# Output: [('Alice', 1), ('Bob', 1), ('Charlie', 1), ('Diana', 0)]
```

## **Key Rules for Aggregates:**
1.  **`func.count(Column)`:** Counts non-NULL values in that column.
2.  **`.group_by(GroupColumn)`:** Mandatory. Defines the groups for the count.
3.  **`isouter=True`:** Use in the join to include groups with zero counts (e.g., empty departments).
---

## **9. The `~` (Tilde) Operator - Negation**

**Purpose:** Invert a condition. It becomes `NOT (condition)` in SQL.

### **Example 1: Anti-Join with `~` and `any()`**
Find departments that have **NO** employees using the relationship.
```python
from sqlalchemy import not_

# Find departments where the 'employees' relationship is EMPTY
result = session.query(Department).filter(
    ~Department.employees.any()
).all()
# Output: [<HR>] (The department with no employees)
```
- `Department.employees.any()`: True if the department has *any* employees.
- `~Department.employees.any()`: True if the department has *no* employees.

### **Example 2: Negating a Filter**
Find employees who are **NOT** named 'Alice'.
```python
result = session.query(Employee).filter(
    ~(Employee.name == 'Alice')
).all()
# Output: [<Bob>, <Charlie>, <Diana>]
```

### **Example 3: Combining with `&` (AND), `|` (OR)**
Find employees not in Engineering OR not in Marketing.
```python
result = session.query(Employee).join(Department).filter(
    ~((Department.name == 'Engineering') | (Department.name == 'Marketing'))
).all()
# Output: [<Diana>] (The employee with no department)
```
---

# **Self-Referential Joins**

## **1. The Concept**
A **self-referential join** links a table to itself. It's used to model hierarchical data (tree structures) where records have a parent-child relationship with others in the same table.
- **Examples:** Organizational charts, category hierarchies, comment threads.

## **2. The Model Setup**
```python
class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    # Foreign key pointing to THIS table's primary key
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'))
    
    # Relationship to the PARENT (the "one" side)
    parent: Mapped["Category"] = relationship(remote_side=[id], back_populates="children")
    
    # Relationship to CHILDREN (the "many" side)
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
```

**Key Parameters:**
- `remote_side=[id]`: Tells SQLAlchemy the foreign key (`parent_id`) points to *this* table's `id` column.
- `back_populates`: Links the two relationships bidirectionally.

## **3. Querying Methods**

### **Method 1: Using the Relationship (Easy)**
Leverage the defined `parent` relationship for automatic joins.
```python
# Get all categories and their parent's name
result = session.query(
    Category.name,
    Category.parent.name  # Access parent's name via relationship
).all()

for cat_name, parent_name in result:
    print(f"Category: {cat_name}, Parent: {parent_name}")
```

### **Method 2: Explicit Self-Join with `aliased` (Full Control)**
Treat the same table as two distinct entities.
```python
from sqlalchemy.orm import aliased

# Create an alias for the parent table
Parent = aliased(Category)

result = session.query(
    Category.name.label("child_name"),
    Parent.name.label("parent_name")
).outerjoin(  # Use OUTERJOIN to include root categories (no parent)
    Parent, Category.parent_id == Parent.id  # Explicit join condition
).all()

for child, parent in result:
    print(f"Child: {child}, Parent: {parent}")
```

## **4. Key Insights**
- **`aliased()` is mandatory** for explicit self-joins to avoid table name ambiguity.
- **Use `outerjoin`** to include root nodes (items with `parent_id = NULL`).
- The relationship method (`Category.parent.name`) is simpler for basic needs.
- The explicit `aliased` method is essential for complex filters or when you need to join the same table multiple times.
---