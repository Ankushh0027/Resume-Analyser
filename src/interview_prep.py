"""
Interview Preparation Data & Curated Question Sheets Module
Provides company-wise interview questions, DSA pattern roadmaps, and Core CS subject cards.
"""

COMPANY_QUESTION_SHEETS = {
    "Google": {
        "tagline": "Emphasis on Advanced DSA, System Scale, & Graph Algorithms",
        "focus_areas": ["Graphs & Trees", "Dynamic Programming", "System Scale", "Clean Code"],
        "top_questions": [
            {"title": "Word Ladder II", "topic": "Graph / BFS", "difficulty": "Hard"},
            {"title": "Trapping Rain Water", "topic": "Two Pointers", "difficulty": "Hard"},
            {"title": "Median of Two Sorted Arrays", "topic": "Binary Search", "difficulty": "Hard"},
            {"title": "Serialize and Deserialize Binary Tree", "topic": "Tree / Design", "difficulty": "Hard"},
            {"title": "Course Schedule I & II", "topic": "Graph / Topological Sort", "difficulty": "Medium"},
            {"title": "LRU Cache Implementation", "topic": "Design / Linked HashMap", "difficulty": "Medium"},
            {"title": "Find Median from Data Stream", "topic": "Heap / Priority Queue", "difficulty": "Hard"},
        ],
        "system_design": [
            "Design Google Drive / Distributed Storage System",
            "Design Google Search Autocomplete / Typeahead Suggestion",
            "Design YouTube Video Transcoding & Streaming Pipeline",
        ]
    },
    "Amazon": {
        "tagline": "Emphasis on Leadership Principles, Object-Oriented Design, & High Availability",
        "focus_areas": ["Leadership Principles (STAR)", "LLD / OOD", "Trees & BST", "Sliding Window"],
        "top_questions": [
            {"title": "Reorganize String", "topic": "Greedy / Heap", "difficulty": "Medium"},
            {"title": "Number of Islands", "topic": "Graph / DFS / BFS", "difficulty": "Medium"},
            {"title": "Lowest Common Ancestor of Binary Tree", "topic": "Tree / DFS", "difficulty": "Medium"},
            {"title": "Word Search II", "topic": "Trie / Backtracking", "difficulty": "Hard"},
            {"title": "Copy List with Random Pointer", "topic": "Linked List", "difficulty": "Medium"},
            {"title": "Critical Connections in a Network", "topic": "Tarjan Graph Algorithm", "difficulty": "Hard"},
            {"title": "Design Search Autocomplete System", "topic": "System Design / Trie", "difficulty": "Hard"},
        ],
        "system_design": [
            "Design Amazon E-Commerce Order Management System",
            "Design Distributed Rate Limiter Service",
            "Design Flash Sale / Inventory Reservation Lock",
        ]
    },
    "Microsoft": {
        "tagline": "Emphasis on String Manipulation, Linked Lists, & Clean Code Quality",
        "focus_areas": ["Strings & Arrays", "Linked Lists", "Tree Traversal", "System Design"],
        "top_questions": [
            {"title": "Reverse Words in a String", "topic": "String", "difficulty": "Medium"},
            {"title": "Rotate Image / Matrix", "topic": "Matrix", "difficulty": "Medium"},
            {"title": "Sign of the Product of an Array", "topic": "Array", "difficulty": "Easy"},
            {"title": "Spiral Matrix", "topic": "Matrix", "difficulty": "Medium"},
            {"title": "Merge Intervals", "topic": "Intervals / Sorting", "difficulty": "Medium"},
            {"title": "Construct Binary Tree from Preorder & Inorder", "topic": "Tree", "difficulty": "Medium"},
            {"title": "Design In-Memory File System", "topic": "Design / Trie", "difficulty": "Hard"},
        ],
        "system_design": [
            "Design Microsoft Teams Real-Time Chat & Video Signaling",
            "Design Azure Blob Storage Access Tiering",
            "Design Distributed Web Crawler",
        ]
    },
    "Meta (Facebook)": {
        "tagline": "Emphasis on High-Speed Solving, Binary Search, & Social Graph Processing",
        "focus_areas": ["Binary Search Variants", "BFS/DFS", "Sliding Window", "High Speed Coding"],
        "top_questions": [
            {"title": "Kth Largest Element in an Array", "topic": "Quickselect / Heap", "difficulty": "Medium"},
            {"title": "Minimum Remove to Make Valid Parentheses", "topic": "Stack / String", "difficulty": "Medium"},
            {"title": "Product of Array Except Self", "topic": "Array / Prefix Sum", "difficulty": "Medium"},
            {"title": "Subarray Sum Equals K", "topic": "Prefix Sum / HashMap", "difficulty": "Medium"},
            {"title": "Binary Tree Right Side View", "topic": "Tree / BFS", "difficulty": "Medium"},
            {"title": "Dot Product of Two Sparse Vectors", "topic": "Two Pointers", "difficulty": "Medium"},
            {"title": "Range Sum of BST", "topic": "BST Traversal", "difficulty": "Easy"},
        ],
        "system_design": [
            "Design Facebook News Feed System",
            "Design Messenger / Real-Time Notification Gateway",
            "Design Instagram Story Viewer & Engagement Counter",
        ]
    },
    "Uber": {
        "tagline": "Emphasis on Geospatial Indexing, Dynamic Programming, & Real-Time Dispatch",
        "focus_areas": ["Geospatial H3/QuadTree", "Graphs & Shortest Path", "Dynamic Programming"],
        "top_questions": [
            {"title": "Bus Routes", "topic": "BFS / Graph", "difficulty": "Hard"},
            {"title": "Sliding Window Maximum", "topic": "Deque / Sliding Window", "difficulty": "Hard"},
            {"title": "Sudoku Solver", "topic": "Backtracking", "difficulty": "Hard"},
            {"title": "Coin Change", "topic": "Dynamic Programming", "difficulty": "Medium"},
            {"title": "Design Leaderboard", "topic": "Heap / HashMap", "difficulty": "Medium"},
        ],
        "system_design": [
            "Design Uber Ride Matching & Dispatch Architecture",
            "Design Real-Time Driver Location Tracking Service",
            "Design Surge Pricing Engine",
        ]
    }
}

DSA_TOPIC_SHEETS = {
    "Arrays & Hashing": [
        "Two Sum / 3Sum / 4Sum",
        "Group Anagrams",
        "Top K Frequent Elements",
        "Encode and Decode Strings",
        "Longest Consecutive Sequence"
    ],
    "Two Pointers & Sliding Window": [
        "Valid Palindrome",
        "Container With Most Water",
        "Longest Substring Without Repeating Characters",
        "Longest Repeating Character Replacement",
        "Minimum Window Substring"
    ],
    "Binary Search": [
        "Search in Rotated Sorted Array",
        "Find Minimum in Rotated Sorted Array",
        "Time Based Key-Value Store",
        "Koko Eating Bananas"
    ],
    "Trees & Graphs": [
        "Invert Binary Tree & Max Depth",
        "Validate Binary Search Tree",
        "Binary Tree Level Order Traversal",
        "Clone Graph & Pacific Atlantic Water Flow",
        "Graph Valid Tree & Number of Connected Components"
    ],
    "Dynamic Programming": [
        "Climbing Stairs & House Robber",
        "Longest Palindromic Substring",
        "Coin Change & Word Break",
        "Longest Increasing Subsequence",
        "Edit Distance & 0/1 Knapsack"
    ]
}

CORE_CS_SUBJECTS = {
    "DBMS & SQL": [
        {"q": "Difference between SQL (Relational) and NoSQL databases?", "a": "Relational DBs (PostgreSQL, MySQL) use structured schemas and ACID transactions, ideal for financial/relational data. NoSQL (MongoDB, DynamoDB) offers horizontal scaling, flexible document/key-value schemas, and eventual consistency."},
        {"q": "What are Database Indexes and how do B-Trees work?", "a": "Indexes speed up data retrieval queries from O(N) full table scans to O(log N) operations using self-balancing B-Trees or B+ Trees, at the cost of slower writes and extra disk storage."},
        {"q": "What are ACID Properties?", "a": "Atomicity (all or nothing), Consistency (valid state rules), Isolation (concurrent transactions don't interfere), and Durability (committed changes persist despite server crashes)."}
    ],
    "Operating Systems": [
        {"q": "Difference between Process and Thread?", "a": "A Process is an executing instance of a program with its own isolated memory space. A Thread is a lightweight execution path within a process that shares virtual memory and resources with sibling threads."},
        {"q": "What is Deadlock and what are the 4 Necessary Conditions?", "a": "Deadlock occurs when processes are blocked waiting for resources held by each other. Conditions: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, and 4) Circular Wait."},
        {"q": "What is Virtual Memory and Paging?", "a": "Virtual Memory provides applications with an illusion of contiguous memory using disk storage. Paging maps virtual address pages to physical memory frames via Page Tables and OS Translation Lookaside Buffers (TLB)."}
    ],
    "System Design": [
        {"q": "How to scale a system from 1,000 to 1,000,000 users?", "a": "1) Separate Web Server and DB. 2) Implement Redis caching. 3) Add Load Balancers & Stateless Web Servers. 4) Use CDN for static assets. 5) Database Read Replicas & Database Sharding."},
        {"q": "Difference between Load Balancing Algorithms (Round Robin vs Consistent Hashing)?", "a": "Round Robin distributes requests sequentially across servers. Consistent Hashing maps keys to servers on a hash ring, minimizing key redistribution when nodes scale in/out (essential for distributed caching)."},
        {"q": "What is CAP Theorem?", "a": "In a distributed system, you can only guarantee 2 of 3 properties simultaneously during network partitions: Consistency (all nodes see same data), Availability (every request receives a response), or Partition Tolerance (system continues despite message drops)."}
    ],
    "Computer Networks": [
        {"q": "Difference between TCP and UDP?", "a": "TCP is connection-oriented, reliable, orders packets, and uses 3-way handshakes (HTTP/HTTPS, SSH, Database connections). UDP is connectionless, fast, has zero overhead, but allows packet drops (Video Streaming, VoIP, Gaming)."},
        {"q": "What happens when you type 'google.com' in browser?", "a": "1) Browser checks cache ➔ 2) DNS Query translates domain to IP ➔ 3) TCP 3-Way Handshake ➔ 4) TLS/SSL Certificate Negotiation ➔ 5) HTTP GET Request ➔ 6) Web Server / CDN Response ➔ 7) Browser renders HTML/CSS/JS DOM."}
    ]
}
