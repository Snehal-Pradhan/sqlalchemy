# {{Question}}

> **Topics:** #core #session

---

> **Status** - `Done` / `Pending`

### ❔ My Question
What is the difference between `session.add()` and `session.commit()`? Why don't my objects have an ID after I add them?

### ✅ The Answer
After research, I learned that `session.add()` stages the object in memory (in the session's "identity map"), but it doesn't talk to the database. `session.commit()` **flushes** all changes to the database, which assigns primary keys and makes the changes permanent.

**See the code:** [./01_session_solution.py](./01_session_solution.py)
