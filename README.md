# Python Assignments - Zala Satyaraj Sinh

**Enrollment Number:** 12402080601125  
**Course:** Programming with Python (202044504)  
**Programme:** B.Tech. Information Technology — Semester V

---

## Repository Structure

```
Python-Assignment/
├── Assignment-1/
│   ├── Q-1.py          # Q1 – Campus Merit Analyzer
│   ├── Q-2.py          # Q2 – Optimized Password Audit
│   ├── Q-3.py          # Q3 – Recursive Expression Engine
│   ├── Q-4.py          # Q4 – Exception-Safe CSV Transaction Splitter
│   ├── Q-5.py          # Q5 – OOP Bank Settlement System
│   ├── Q-6.py          # Q6 – Module Dependency Resolver
│   ├── Q-7.py          # Q7 – Interactive Formula Validator
│   ├── Q-8.py          # Q8 – Compressed Log Index (Pickle + ZIP)
│   ├── Q-9.py          # Q9 – Threaded Job Scheduler Simulation
│   ├── Q-10.py         # Q10 – Tkinter Assignment Tracker
│   ├── Transaction.csv # Sample input for Q-4
│   ├── credit.csv      # Output of Q-4
│   ├── debit.csv       # Output of Q-4
│   ├── error.csv       # Output of Q-4
│   ├── submissions.json# Persistent data for Q-10
│   ├── archive.pkl     # Pickle index built by Q-8
│   ├── archive.zip     # ZIP archive built by Q-8
│   └── Logs/
│       ├── Server1.txt
│       ├── Server2.txt
│       └── Server3.txt
│
├── Assignment-2/
│   ├── Q-1.py          # Q1 – Email Extractor (Regex)
│   ├── Q-2.py          # Q2 – HTML Product Scraper & Ranker
│   ├── Q-3.py          # Q3 – MySQL Student Database (CRUD)
│   ├── Q-4.py          # Q4 – Safe Dynamic SQL Query Builder
│   ├── Q-5.py          # Q5 – MySQL Contact Manager (Tkinter GUI)
│   ├── Q-6.py          # Q6 – Suspicious Login Detector
│   ├── Q-7.py          # Q7 – IoT ETL Pipeline (JSONL)
│   ├── Q-8.py          # Q8 – Grid Path DP (Max Score + Ways)
│   ├── Q-9.py          # Q9 – Inventory Management (OOP)
│   ├── Q-10.py         # Q10 – Marks Analyser (pandas + matplotlib)
│   ├── Emails.txt
│   ├── Data.jsonl
│   ├── Marks.csv
│   ├── Student.csv
│   ├── Registration.csv
│   ├── Page1.html
│   ├── Page2.html
│   └── output/
│       ├── cleaned_marks.csv
│       ├── summary.csv
│       ├── grade_distribution.png
│       ├── subject_average.png
│       └── top_performers.png
│
└── README.md
```

---

## Assignment 1

**Course:** Programming with Python (202044504)  
**Prerequisites:** Python 3.10+ (standard library only; `tkinter` is bundled with Python on Windows)

---

### Q-1. Campus Merit Analyzer using Compound Data Structures

| Field | Details |
|-------|---------|
| Difficulty | Advanced University / Placement |
| CO Mapping | CO-2, CO-4 |
| Bloom Level | L4 Analyze |
| Skills Tested | Lists, tuples, dictionaries, sorting, hashing, data aggregation |

**Problem Statement:**  
You are given records of students in the form enrollment, name, semester, CPI and a list of subject marks. Build a program that stores the records using lists, tuples and dictionaries. For each semester, print the top K students by CPI. If CPI is the same, prefer the student with higher average marks; if still tied, prefer lexicographically smaller enrollment number. Also print the subject-wise topper for every subject code.

**Input Format:** First line: `n k m`. Next n lines: `enrollment name semester cpi` followed by m integer marks. Subject codes are S1 to Sm.

**Output Format:** Semester-wise top K enrollments in sorted order, followed by subject-wise toppers.

**Constraints:** `1 <= n <= 100000, 1 <= k <= 50, 1 <= m <= 12, 1 <= semester <= 8, 0 <= marks <= 100, 0.0 <= cpi <= 10.0`

**Run:**
```
python Q-1.py
```

**Sample Input:**
```
5 2 3
2201 Asha 5 8.90 90 82 75
2202 Bharat 5 8.90 88 95 70
2203 Chaitra 3 9.10 91 88 92
2204 Dev 5 7.80 76 80 85
2205 Esha 3 9.10 91 90 88
```

**Sample Output:**
```
Semester 3: 2205 2203
Semester 5: 2202 2201
S1: 2203 2205
S2: 2202
S3: 2203
```

**Expected Complexity:** Time O(n·m + n log n) | Space O(n·m)

**Test Cases:**
| # | Test | Input | Expected |
|---|------|-------|----------|
| 1 | Sample | 5 students, 2 semesters, 3 subjects | As above |
| 2 | Boundary | n=1, k=1, m=1 — single student | That student is both top-K and subject topper |
| 3 | CPI tie with avg-marks tiebreak | Two students same CPI, different avg marks | Higher avg listed first |
| 4 | Full tie (CPI + avg) | Same CPI and avg → enrollment tiebreak | Lex smaller enrollment first |
| 5 | All students same semester | All in semester 1, k=3 | Top 3 printed |

---

### Q-2. Optimized Password Audit with Pattern Constraints

| Field | Details |
|-------|---------|
| Difficulty | Product-Based Company Level |
| CO Mapping | CO-1, CO-3 |
| Bloom Level | L5 Evaluate |
| Skills Tested | Strings, regular expressions, hashing/trie, validation, edge-case analysis |

**Problem Statement:**  
Given n candidate passwords, classify each as `STRONG`, `WEAK_LENGTH`, `WEAK_PATTERN` or `COMPROMISED`. A strong password must contain at least one lowercase letter, uppercase letter, digit and one special symbol from `$#@`. Its length must be between 6 and 12. It must not contain any dictionary word from a banned list as a contiguous substring, ignoring case. It must also not contain the same character more than 3 times consecutively.

**Input Format:** First line: `b`. Next b lines: banned words. Next line: `n`. Next n lines: one password per line.

**Output Format:** For each password, print `password_index: classification`.

**Constraints:** `1 <= b <= 10000, total banned chars <= 200000, 1 <= n <= 100000, password length <= 100`

**Run:**
```
python Q-2.py
```

**Sample Input:**
```
2
admin
college
5
Abc12@
adminA1@
AAAA1@b
short
Good9#
```

**Sample Output:**
```
1: STRONG
2: COMPROMISED
3: WEAK_PATTERN
4: WEAK_LENGTH
5: STRONG
```

**Expected Complexity:** Time O(total password length + total banned length) using Trie | Space O(total banned length)

**Test Cases:**
| # | Test | Password | Expected |
|---|------|----------|----------|
| 1 | Sample — strong | Abc12@ | 1: STRONG |
| 2 | Banned substring | adminA1@ | 2: COMPROMISED |
| 3 | 4 consecutive chars | AAAA1@b | 3: WEAK_PATTERN |
| 4 | Too short | short | 4: WEAK_LENGTH |
| 5 | Boundary len=6 | Ab1$cD | STRONG |
| 6 | Boundary len=12 | Ab1$cDefGh2# | STRONG |
| 7 | Missing special char | Password1 | WEAK_PATTERN |

---

### Q-3. Recursive Expression Engine with Memoization

| Field | Details |
|-------|---------|
| Difficulty | FAANG Interview Level |
| CO Mapping | CO-1, CO-2 |
| Bloom Level | L6 Create |
| Skills Tested | Recursion, stacks, dictionaries, parsing, memoization, cycle detection |

**Problem Statement:**  
Implement a recursive expression evaluator for integer expressions containing non-negative integers, `+`, `-`, `*`, parentheses and variable references. Each variable may be defined by another expression. Detect cyclic variable dependencies and report `CYCLE`. Use memoization so that repeated variable evaluations are not recomputed.

**Input Format:** First line: `v`. Next v lines: `variable_name = expression`. Last line: `expression_to_evaluate`.

**Output Format:** The integer value, or `CYCLE` if cyclic dependency exists, or `INVALID` if expression syntax is invalid.

**Constraints:** `1 <= v <= 200000, expression length total <= 500000, values fit in signed 64-bit integer`

**Run:**
```
python Q-3.py
```

**Sample Input:**
```
3
a = 2 + 3
b = a * 4
c = b - (a + 1)
c + 10
```

**Sample Output:** `24`

**Sample Explanation:** a = 5, b = 20, c = 14, c + 10 = 24.

**Expected Complexity:** Time O(total expression length) | Space O(total expression length)

**Test Cases:**
| # | Test | Input | Expected |
|---|------|-------|----------|
| 1 | Sample | a=2+3, b=a*4, c=b-(a+1), eval c+10 | 24 |
| 2 | Cycle | a=b+1, b=a*2, eval a | CYCLE |
| 3 | Invalid syntax | a=2++3 | INVALID |
| 4 | Parentheses nesting | x=(2+3)*(4-1) | 15 |
| 5 | Deep variable chain | a=1, b=a+1, c=b+1, d=c+1, eval d | 4 |

---

### Q-4. Exception-Safe CSV Transaction Splitter

| Field | Details |
|-------|---------|
| Difficulty | Advanced University / Industry |
| CO Mapping | CO-1, CO-4 |
| Bloom Level | L5 Evaluate |
| Skills Tested | File handling, CSV, exception handling, dictionaries, sorting, data cleaning |

**Problem Statement:**  
A CSV file contains transaction_id, account_id, type, amount and timestamp. Create a program that reads the file, validates every row, writes valid credit and debit transactions into separate CSV files, writes rejected rows into `error.csv` with reason, and finally prints account-wise balance changes. The program must continue processing after invalid rows using exception handling.

**Input Format:** Path of input CSV file with header row followed by records.

**Output Format:** `credit.csv`, `debit.csv`, `error.csv` and console summary of account-wise net amount in descending order of absolute balance change.

**Constraints:** `1 <= rows <= 1000000, amount > 0, type is CREDIT or DEBIT, timestamp is ISO-like yyyy-mm-ddThh:mm:ss`

**Input file:** `Transaction.csv`  
**Output files:** `credit.csv`, `debit.csv`, `error.csv`

**Run:**
```
python Q-4.py
# Enter CSV file path: Transaction.csv
```

**Sample Input (Transaction.csv):**
```
tid,acc,type,amount,time
T1,A1,CREDIT,500,2026-01-01T10:00:00
T2,A1,DEBIT,abc,2026-01-01T10:05:00
T3,A2,DEBIT,100,2026-01-01T10:10:00
```

**Sample Output (console):**
```
A1 500
A2 -100
```

**Expected Complexity:** Time O(r log a) | Space O(a)

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | Mixed valid + invalid | A1 500, A2 -100; T2 → error.csv |
| 2 | Non-numeric amount | amount = "abc" | Row → error.csv with reason |
| 3 | Invalid type | type = "TRANSFER" | Row → error.csv |
| 4 | Missing field | Empty acc column | Row → error.csv |
| 5 | All valid | No errors | error.csv is empty (header only) |

---

### Q-5. Object-Oriented Bank Settlement System

| Field | Details |
|-------|---------|
| Difficulty | Product-Based Company Level |
| CO Mapping | CO-1, CO-2 |
| Bloom Level | L6 Create |
| Skills Tested | OOP, encapsulation, custom exceptions, rollback logic, dictionaries |

**Problem Statement:**  
Design an OOP-based settlement engine with Account, Transaction and Bank classes. The engine must support deposit, withdraw and transfer operations, maintain transaction history, prevent overdraft, and rollback an entire batch if any transaction in the batch fails. Use custom exceptions and suitable getters/setters or properties.

**Input Format:** Initial accounts followed by q operations: `DEPOSIT acc amount`, `WITHDRAW acc amount`, `TRANSFER from to amount`, or `BATCH_BEGIN`/`BATCH_END`.

**Output Format:** Final balance of all accounts in account_id order, and `FAILED` batch number if any batch was rolled back.

**Constraints:** `1 <= accounts <= 100000, 1 <= q <= 300000, amount <= 10^9, all balances fit in 64-bit integer`

**Run:**
```
python Q-5.py
```

**Sample Input:**
```
3
A 1000
B 200
C 0
5
TRANSFER A B 300
BATCH_BEGIN
WITHDRAW B 1000
DEPOSIT C 50
BATCH_END
```

**Sample Output:**
```
FAILED 1
A 700
B 500
C 0
```

**Sample Explanation:** The batch fails because B cannot withdraw 1000. The deposit to C is rolled back.

**Expected Complexity:** Time O(q + n log n) | Space O(n + batch_size)

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | Transfer + failed batch | FAILED 1; correct balances |
| 2 | Overdraft prevention | WITHDRAW more than balance | Error; balance unchanged |
| 3 | Successful batch | All ops valid inside batch | Committed normally |
| 4 | Account not found | DEPOSIT to unknown account | Error raised |
| 5 | Multi-batch rollback | Two batches, one fails | Only failed batch listed |

---

### Q-6. Python Module Dependency Resolver

| Field | Details |
|-------|---------|
| Difficulty | FAANG Interview Level |
| CO Mapping | CO-1, CO-2 |
| Bloom Level | L4 Analyze |
| Skills Tested | Graphs, topological sorting, heaps, sets, dictionaries, cycle detection |

**Problem Statement:**  
Given a set of Python module names and import relationships, determine a valid loading order. If a circular dependency exists, print `CYCLE` and the modules involved in one cycle. Ignore duplicate import edges. If multiple modules can be loaded, choose lexicographically smallest module first.

**Input Format:** First line: `n e`. Next n lines: module name. Next e lines: `module_a imports module_b`.

**Output Format:** Lexicographically smallest valid loading order, or `CYCLE` followed by one detected cycle.

**Constraints:** `1 <= n <= 200000, 0 <= e <= 500000, module name length <= 50`

**Run:**
```
python Q-6.py
```

**Sample Input:**
```
4 3
core
db
ui
auth
ui auth
auth db
db core
```

**Sample Output:** `core db auth ui`

**Sample Explanation:** core has no dependency. db depends on core, auth depends on db and ui depends on auth.

**Expected Complexity:** Time O((n+e) log n) | Space O(n+e)

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | Linear chain of dependencies | core db auth ui |
| 2 | No edges | 3 standalone modules | Lexicographic order |
| 3 | Cycle | A imports B, B imports A | CYCLE A B A |
| 4 | Duplicate edges | Same import listed twice | Ignored; correct order |
| 5 | Disconnected | Two separate components | Both sorted and merged |

---

### Q-7. Interactive Formula Validator with Custom Exceptions

| Field | Details |
|-------|---------|
| Difficulty | Advanced University / Placement |
| CO Mapping | CO-1, CO-2 |
| Bloom Level | L5 Evaluate |
| Skills Tested | Exception handling, assertions, dictionaries, parsing, interactive programs |

**Problem Statement:**  
Build an interactive calculator that accepts formulas of the form `operand operator operand`. Operands may be integers, decimals or previously stored variables. Supported operators are `+`, `-`, `*`, `/` and `%`. Invalid format, unknown variables, division by zero and unsupported operators must raise separate custom exceptions. The calculator must continue until the user enters `quit`.

**Input Format:** Multiple lines containing formulas, assignment statements (e.g. `x = 10`), or `quit`.

**Output Format:** For each valid formula, print the result. For invalid lines, print the exception type.

**Constraints:** `Up to 100000 input lines; variable names follow Python identifier rules; values fit in float range`

**Run:**
```
python Q-7.py
```

**Sample Input:**
```
x = 10
x + 5
x / 0
3 ** 2
quit
```

**Sample Output:**
```
15
DivisionByZeroError
UnsupportedOperatorError
```

**Expected Complexity:** Time O(1) per formula | Space O(v) where v = number of variables

**Test Cases:**
| # | Test | Input | Expected |
|---|------|-------|----------|
| 1 | Valid expression | x=10, x+5 | 15 |
| 2 | Division by zero | x / 0 | DivisionByZeroError |
| 3 | Unsupported operator | 3 ** 2 | UnsupportedOperatorError |
| 4 | Unknown variable | z + 1 | UnknownVariableError |
| 5 | Modulo by zero | x % 0 | DivisionByZeroError |

---

### Q-8. Compressed Log Index using Pickle and Zip

| Field | Details |
|-------|---------|
| Difficulty | Advanced University / Industry |
| CO Mapping | CO-1, CO-4 |
| Bloom Level | L6 Create |
| Skills Tested | File handling, pickling, zip/unzip, dictionaries, text processing, indexing |

**Problem Statement:**  
A server produces several text log files. Create a program that scans all files in a folder, builds an inverted index mapping each normalized token to the list of file names and line numbers where it appears, stores the index using pickle, and compresses both original logs and index into a zip file. The program must also support a search mode that loads the pickle index and answers token queries.

**Input Format:** Mode `BUILD` or `SEARCH`. BUILD receives folder path and output zip name. SEARCH receives pickle path and q query tokens.

**Output Format:** In BUILD mode: total files, total lines, unique tokens. In SEARCH mode: all file:line matches per token.

**Constraints:** `1 <= files <= 10000, total lines <= 5000000, token length <= 50`

**Input directory:** `Logs/`

**Run:**
```
python Q-8.py
# BUILD Logs archive.zip

python Q-8.py
# SEARCH archive.pkl 2 error timeout
```

**Sample Output (BUILD):**
```
FILES 3
LINES 1200
TOKENS 845
```

**Expected Complexity:** Time O(total characters in all files) | Space O(unique tokens + postings)

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Build | 3 log files in Logs/ | FILES 3 + correct LINES/TOKENS |
| 2 | Search found | Token exists in index | filename:line_no entries listed |
| 3 | Search not found | Token absent | NOT FOUND |
| 4 | Empty directory | No files | FILES 0, LINES 0, TOKENS 0 |
| 5 | Case insensitive | Search "ERROR" | Matches "error" in logs |

---

### Q-9. Threaded Job Scheduler Simulation

| Field | Details |
|-------|---------|
| Difficulty | Product-Based Company Level |
| CO Mapping | CO-1, CO-2 |
| Bloom Level | L5 Evaluate |
| Skills Tested | Multithreading concepts, priority queues, simulation, synchronization design |

**Problem Statement:**  
Simulate a job scheduler where each job has job_id, priority, duration and required resource count. Multiple worker threads execute jobs. Higher priority jobs must be processed first; jobs with same priority use earlier arrival order. The program must maintain thread-safe job assignment and produce a final execution report.

**Input Format:** First line: `w n`. Next n lines: `arrival_time job_id priority duration resources`.

**Output Format:** For each job: `job_id worker_id start_time finish_time`. Finally: `AVG_WAIT <average>`.

**Constraints:** `1 <= w <= 64, 1 <= n <= 200000, 1 <= duration <= 10^6, 1 <= resources <= 100`

**Run:**
```
python Q-9.py
```

**Sample Input:**
```
2 3
0 J1 2 5 1
1 J2 5 3 1
2 J3 2 2 1
```

**Sample Output:**
```
J1 W1 0 5
J2 W2 1 4
J3 W2 4 6
AVG_WAIT 0.67
```

**Sample Explanation:** J2 has higher priority and is assigned when a worker is available. J3 waits until W2 becomes free.

**Expected Complexity:** Time O(n log n) | Space O(n + w)

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | 2 workers, 3 jobs | As above |
| 2 | 1 worker | All jobs sequential | Wait times accumulate |
| 3 | Same priority | Multiple same-priority jobs | Earlier arrival wins |
| 4 | All arrive at t=0 | Simultaneous | Highest priority first |
| 5 | Late arrival | Job arrives after workers free | Zero wait |

---

### Q-10. Tkinter Assignment Tracker with File Persistence

| Field | Details |
|-------|---------|
| Difficulty | Advanced University / Mini Project |
| CO Mapping | CO-1, CO-4, CO-5 |
| Bloom Level | L6 Create |
| Skills Tested | Tkinter, GUI design, event handling, file persistence, validation, CSV/JSON |

**Problem Statement:**  
Create a Tkinter GUI application to manage student assignment submissions. The application must support adding a student, adding a submission, updating marks, filtering by pending/completed status, and exporting a CSV report. Data must persist locally using JSON or CSV files. Input fields must be validated before saving.

**Input Format:** GUI inputs through Entry, Text, Radio Button, Check Button, Listbox/Menu or Combobox widgets.

**Output Format:** Interactive GUI plus exported CSV report with enrollment, name, assignment, status, marks and remarks.

**Constraints:** At least 5 widgets. Must handle 5000+ records without freezing during filtering.

**Data file:** `submissions.json` (auto-created)

**Run:**
```
python Q-10.py
```
No extra packages — uses Python's built-in `tkinter`.

**Test Cases:**
| # | Test | Action | Expected |
|---|------|--------|----------|
| 1 | Add without marks | Submit with empty marks | Status = Pending |
| 2 | Add with marks | Submit with marks = 18 | Status = Completed |
| 3 | Update marks | Select Pending row, enter marks | Status → Completed |
| 4 | Filter | Select "Pending" | Only pending rows shown |
| 5 | Export CSV | Click Export | CSV file created with all records |

---

## Assignment 2

### Prerequisites
```bash
pip install mysql-connector-python pandas matplotlib
```
> Q-1, Q-2, Q-6, Q-7, Q-8, Q-9 — **standard library only**  
> Q-3, Q-4, Q-5 — require `mysql-connector-python` + running MySQL server  
> Q-10 — requires `pandas` and `matplotlib`

---

### Q-1. Email Extractor using Regular Expressions

**What it does:** Scans a text file and extracts all valid email addresses with `.com`, `.edu`, `.org` TLDs using a compiled regex. Groups by TLD and prints count + lexicographically smallest address per group.

**Input:** `Emails.txt` (command-line argument)

**Run:**
```
python Q-1.py Emails.txt
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | Mixed emails in file | Correct counts per TLD |
| 2 | No valid emails | File with no matches | No output |
| 3 | Duplicates | Same email repeated | Counted once |
| 4 | Case normalize | USER@EXAMPLE.COM | Lowered to user@example.com |
| 5 | Mixed TLDs | .com, .edu, .org present | Three lines printed |

---

### Q-2. HTML Product Scraper & Ranker

**What it does:** Parses HTML product pages using Python's built-in `html.parser`. Extracts product name, normalised price, and rating. Deduplicates by name (best rating wins; tie → lower price). Prints top-K ranked products.

**Input:** `Page1.html`, `Page2.html` (via stdin)

**Run:**
```
python Q-2.py
# stdin: 2 3
#        Page1.html
#        Page2.html
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | 2 pages, k=3 | Top 3 products ranked |
| 2 | k=1 | Only top product | Single output line |
| 3 | Duplicate product | Same product in both pages | Best rating kept |
| 4 | Price with comma | $1,299.50 | Parsed as 1299.5 |
| 5 | Missing rating | Product without rating tag | Skipped |

---

### Q-3. MySQL Student Database (CRUD)

**What it does:** Connects to MySQL, creates Student and CourseRegistration tables, bulk-inserts from CSV, then queries students in a course above an SPI threshold.

**Input files:** `Student.csv`, `Registration.csv`

**Database Schema:**
```sql
CREATE TABLE Student (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    spi DECIMAL(3,1) NOT NULL
);
CREATE TABLE CourseRegistration (
    student_id INT,
    course_id VARCHAR(20),
    PRIMARY KEY (student_id, course_id)
);
```

**Run:**
```
pip install mysql-connector-python
python Q-3.py
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | PY101, threshold 8.0 | Matching students listed |
| 2 | High threshold | threshold = 10 | No results |
| 3 | Empty CSV | No rows | No error, empty result |
| 4 | Duplicate key | Same student_id twice | ON DUPLICATE KEY UPDATE |
| 5 | Wrong course | Non-existent course | No results |

---

### Q-4. Safe Dynamic SQL Query Builder

**What it does:** Builds fully parameterised SQL queries using a column whitelist — prevents SQL injection. Validates columns, operators, sort direction, and row limit.

**Run:**
```
python Q-4.py
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Valid query | Filter by course.id | SQL_OK + results |
| 2 | Invalid column | "student.password" | ValueError |
| 3 | Injection attempt | "id; DROP TABLE" | ValueError |
| 4 | Limit out of range | limit=5000 | ValueError |
| 5 | LIKE operator | Filter with LIKE | Correct WHERE clause |

---

### Q-5. MySQL Contact Manager (Tkinter GUI)

**What it does:** Full CRUD contact manager backed by MySQL with Tkinter GUI. Supports add, update, delete, search by name/email/phone, category dropdown. Email validated with regex.

**Database Schema:**
```sql
CREATE TABLE Contact (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    category VARCHAR(30),
    notes TEXT
);
```

**Run:**
```
pip install mysql-connector-python
python Q-5.py
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Add contact | Valid name + email | Record inserted |
| 2 | Duplicate email | Same email again | Error: Email exists |
| 3 | Invalid email | "notanemail" | Error: Invalid email |
| 4 | Search | Partial name search | Matching contacts shown |
| 5 | Delete | Select + Delete | Record removed |

---

### Q-6. Suspicious Login Detector

**What it does:** Reads timestamped login logs. Flags a user as suspicious when >= X failures within T minutes followed by a success from a different IP. Uses a deque-based sliding window.

**Log format:** `HH:MM <user> <ip> FAIL|SUCCESS`

**Run:**
```
python Q-6.py
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | 3 fails + different-IP success | User flagged |
| 2 | Same IP | Fails + success same IP | Not flagged |
| 3 | Outside window | Old fails (> T min) | Not flagged |
| 4 | X=1 | 1 fail then diff-IP success | Flagged |
| 5 | Multiple users | Two users, one suspicious | Only suspicious one printed |

---

### Q-7. IoT ETL Pipeline (JSONL)

**What it does:** Streams JSONL sensor records. Per device: computes min/max/avg temperature (Celsius), counts valid + corrupted records. Handles invalid JSON, missing fields, non-numeric values.

**Input:** `Data.jsonl`

**Run:**
```
python Q-7.py
# Enter JSONL file path: Data.jsonl
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | Mixed valid + corrupt | Per-device stats |
| 2 | All corrupt | Every line invalid | count=0, corrupted counts |
| 3 | Missing field | No humidity key | Counted as corrupted |
| 4 | Non-numeric temp | "temperature_c": "hot" | Counted as corrupted |
| 5 | Single device | One device, 5 records | Correct min/max/avg |

---

### Q-8. Grid Path DP (Max Score + Count of Ways)

**What it does:** Dynamic programming on N×M grid. Moves: right, down, diagonal. Blocked cells = `X`. Finds max score AND number of paths achieving it (mod 10^9+7). Prints `IMPOSSIBLE` if unreachable.

**Run:**
```
python Q-8.py
```

**Sample Input:**
```
3 3
1 2 3
4 X 6
7 8 9
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | 3×3 with one X | Max score + way count |
| 2 | All blocked | No path | IMPOSSIBLE |
| 3 | Single cell | 1×1, value 5 | 5 1 |
| 4 | Multiple paths | Open 3×3 | Correct count |
| 5 | Diagonal only | Other cells blocked | Single path |

---

### Q-9. Inventory Management (OOP + Operator Overloading)

**What it does:** `Product` and `Inventory` classes with add/delete/update operations, `total_value()`, `__lt__` comparison, and `__add__` merge (combines stock, min purchase price, max selling price).

**Run:**
```
python Q-9.py
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Merge | Same product from two inventories | Combined stock + best prices |
| 2 | Empty | Merge with empty inventory | Original unchanged |
| 3 | Compare | inv_a < inv_b | Correct True/False |
| 4 | Delete | Remove existing product | Removed from inventory |
| 5 | Update stock | Set new quantity | Stock updated |

---

### Q-10. Marks Analyser (pandas + matplotlib)

**What it does:** Reads student marks CSV, cleans invalid/missing data, computes Total/Average/Grade, saves cleaned CSV + summary CSV, generates bar charts (grade distribution, subject averages, top performers).

**Input:** `Marks.csv` | **Output:** `output/` folder

**Run:**
```
pip install pandas matplotlib
python Q-10.py
# Enter CSV file path: Marks.csv
# Enter output folder path: output
```

**Test Cases:**
| # | Test | Scenario | Expected |
|---|------|----------|----------|
| 1 | Sample | Marks.csv | All outputs generated |
| 2 | Missing marks | NaN in subject | Replaced with avg |
| 3 | Out-of-range | Mark = 150 | Replaced with avg |
| 4 | 1 student | Single row | Charts still work |
| 5 | All same grade | All avg >= 90 | Single A+ bar |

---

## Important Notes

- **MySQL Credentials:** Assignment-2 Q-4 and Q-5 have hardcoded credentials. Update `DB_CONFIG` or the `connect()` call to match your local MySQL setup.
- **Auto-created files:** `submissions.json`, `credit.csv`, `debit.csv`, `error.csv`, `archive.pkl`, `archive.zip` are generated by running their respective scripts.
- All programs include **input validation**, **meaningful function names**, and **comments on key logic blocks** as required.
