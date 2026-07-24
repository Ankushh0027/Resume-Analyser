"""
Interview Preparation Data & Curated Question Sheets Module
Provides comprehensive company-wise interview sheets, 10 DSA topic roadmaps with optimal solutions,
direct LeetCode URLs, and Core CS fundamentals with interactive preparation tracking support.
"""

COMPANY_QUESTION_SHEETS = {
    "Google": {
        "tagline": "Emphasis on Advanced Graph Algorithms, Dynamic Programming & System Scale",
        "focus_areas": ["Graphs & Topological Sort", "Dynamic Programming", "Tries & Heaps", "System Architecture"],
        "top_questions": [
            {"id": "goog_1", "title": "Word Ladder II", "topic": "Graph / BFS + Backtracking", "difficulty": "Hard", "complexity": "Time: O(N * M), Space: O(N * M)", "url": "https://leetcode.com/problems/word-ladder-ii/"},
            {"id": "goog_2", "title": "Trapping Rain Water", "topic": "Two Pointers / Stack", "difficulty": "Hard", "complexity": "Time: O(N), Space: O(1)", "url": "https://leetcode.com/problems/trapping-rain-water/"},
            {"id": "goog_3", "title": "Median of Two Sorted Arrays", "topic": "Binary Search", "difficulty": "Hard", "complexity": "Time: O(log(min(M,N))), Space: O(1)", "url": "https://leetcode.com/problems/median-of-two-sorted-arrays/"},
            {"id": "goog_4", "title": "Serialize & Deserialize Binary Tree", "topic": "Tree / Design / BFS", "difficulty": "Hard", "complexity": "Time: O(N), Space: O(N)", "url": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/"},
            {"id": "goog_5", "title": "Course Schedule I & II", "topic": "Graph / Topological Sort", "difficulty": "Medium", "complexity": "Time: O(V + E), Space: O(V + E)", "url": "https://leetcode.com/problems/course-schedule-ii/"},
            {"id": "goog_6", "title": "LRU Cache Implementation", "topic": "Design / Doubly Linked List + Hash", "difficulty": "Medium", "complexity": "Time: O(1), Space: O(Capacity)", "url": "https://leetcode.com/problems/lru-cache/"},
            {"id": "goog_7", "title": "Find Median from Data Stream", "topic": "Heap / Dual Priority Queue", "difficulty": "Hard", "complexity": "Time: O(log N), Space: O(N)", "url": "https://leetcode.com/problems/find-median-from-data-stream/"},
            {"id": "goog_8", "title": "Longest Increasing Path in a Matrix", "topic": "Graph DFS + Memoization", "difficulty": "Hard", "complexity": "Time: O(M * N), Space: O(M * N)", "url": "https://leetcode.com/problems/longest-increasing-path-in-a-matrix/"},
            {"id": "goog_9", "title": "Snapshot Array", "topic": "Binary Search / Design", "difficulty": "Medium", "complexity": "Time: O(log S), Space: O(N + S)", "url": "https://leetcode.com/problems/snapshot-array/"},
            {"id": "goog_10", "title": "Count of Smaller Numbers After Self", "topic": "Merge Sort / Fenwick Tree", "difficulty": "Hard", "complexity": "Time: O(N log N), Space: O(N)", "url": "https://leetcode.com/problems/count-of-smaller-numbers-after-self/"},
        ],
        "system_design": [
            "Design Google Drive / Distributed Blob Storage System (GFS architecture)",
            "Design Google Search Autocomplete / Typeahead Suggestion Engine (Trie + Redis)",
            "Design YouTube Video Transcoding & HLS Streaming Pipeline",
            "Design Distributed Rate Limiter with Token Bucket Algorithm",
        ]
    },
    "Amazon": {
        "tagline": "Emphasis on Leadership Principles (STAR), Object-Oriented Design & High Availability",
        "focus_areas": ["Leadership Principles (STAR)", "LLD / OOD Design", "Trees & BST", "Sliding Window"],
        "top_questions": [
            {"id": "amzn_1", "title": "Reorganize String", "topic": "Greedy / Max Heap", "difficulty": "Medium", "complexity": "Time: O(N log A), Space: O(A)", "url": "https://leetcode.com/problems/reorganize-string/"},
            {"id": "amzn_2", "title": "Number of Islands", "topic": "Graph / BFS / DFS", "difficulty": "Medium", "complexity": "Time: O(M * N), Space: O(M * N)", "url": "https://leetcode.com/problems/number-of-islands/"},
            {"id": "amzn_3", "title": "Lowest Common Ancestor of Binary Tree", "topic": "Tree / DFS Recursion", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(H)", "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/"},
            {"id": "amzn_4", "title": "Word Search II", "topic": "Trie + Backtracking", "difficulty": "Hard", "complexity": "Time: O(M * N * 4^L), Space: O(K * L)", "url": "https://leetcode.com/problems/word-search-ii/"},
            {"id": "amzn_5", "title": "Copy List with Random Pointer", "topic": "Linked List / Hash Map", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(N)", "url": "https://leetcode.com/problems/copy-list-with-random-pointer/"},
            {"id": "amzn_6", "title": "Critical Connections in a Network", "topic": "Tarjan's Bridge Algorithm", "difficulty": "Hard", "complexity": "Time: O(V + E), Space: O(V + E)", "url": "https://leetcode.com/problems/critical-connections-in-a-network/"},
            {"id": "amzn_7", "title": "Design Search Autocomplete System", "topic": "Design / Trie + Priority Queue", "difficulty": "Hard", "complexity": "Time: O(K log 3), Space: O(N * L)", "url": "https://leetcode.com/problems/design-search-autocomplete-system/"},
            {"id": "amzn_8", "title": "Sliding Window Maximum", "topic": "Monotonic Deque", "difficulty": "Hard", "complexity": "Time: O(N), Space: O(K)", "url": "https://leetcode.com/problems/sliding-window-maximum/"},
            {"id": "amzn_9", "title": "K Closest Points to Origin", "topic": "Heap / QuickSelect", "difficulty": "Medium", "complexity": "Time: O(N log K), Space: O(K)", "url": "https://leetcode.com/problems/k-closest-points-to-origin/"},
            {"id": "amzn_10", "title": "Rotting Oranges", "topic": "Multi-Source BFS", "difficulty": "Medium", "complexity": "Time: O(M * N), Space: O(M * N)", "url": "https://leetcode.com/problems/rotting-oranges/"},
        ],
        "system_design": [
            "Design Amazon E-Commerce Order Management & Inventory Locking System",
            "Design Distributed Rate Limiter Service",
            "Design Flash Sale / High-Concurrency Ticket Reservation Engine",
            "Design Key-Value Storage Engine (Dynamo DB Architecture)",
        ]
    },
    "Microsoft": {
        "tagline": "Emphasis on String Processing, Matrix Manipulations, & Clean Code Quality",
        "focus_areas": ["Strings & Arrays", "Matrix Traversals", "Linked Lists", "System Scalability"],
        "top_questions": [
            {"id": "msft_1", "title": "Reverse Words in a String", "topic": "String / Two Pointers", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(N)", "url": "https://leetcode.com/problems/reverse-words-in-a-string/"},
            {"id": "msft_2", "title": "Rotate Image", "topic": "Matrix Manipulation", "difficulty": "Medium", "complexity": "Time: O(N^2), Space: O(1)", "url": "https://leetcode.com/problems/rotate-image/"},
            {"id": "msft_3", "title": "Spiral Matrix", "topic": "Matrix Simulation", "difficulty": "Medium", "complexity": "Time: O(M * N), Space: O(1)", "url": "https://leetcode.com/problems/spiral-matrix/"},
            {"id": "msft_4", "title": "Merge Intervals", "topic": "Sorting / Intervals", "difficulty": "Medium", "complexity": "Time: O(N log N), Space: O(N)", "url": "https://leetcode.com/problems/merge-intervals/"},
            {"id": "msft_5", "title": "Construct Tree from Preorder & Inorder", "topic": "Binary Tree / Hash Index", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(N)", "url": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/"},
            {"id": "msft_6", "title": "Design In-Memory File System", "topic": "Object Oriented Design / Trie", "difficulty": "Hard", "complexity": "Time: O(L log K), Space: O(N)", "url": "https://leetcode.com/problems/design-in-memory-file-system/"},
            {"id": "msft_7", "title": "Find All Anagrams in a String", "topic": "Sliding Window / Hash", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(1)", "url": "https://leetcode.com/problems/find-all-anagrams-in-a-string/"},
            {"id": "msft_8", "title": "Group Anagrams", "topic": "Hash Map / Frequency Array", "difficulty": "Medium", "complexity": "Time: O(N * L), Space: O(N * L)", "url": "https://leetcode.com/problems/group-anagrams/"},
            {"id": "msft_9", "title": "Validate Binary Search Tree", "topic": "Tree DFS Bounds Check", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(H)", "url": "https://leetcode.com/problems/validate-binary-search-tree/"},
            {"id": "msft_10", "title": "Coin Change", "topic": "Dynamic Programming", "difficulty": "Medium", "complexity": "Time: O(N * Amount), Space: O(Amount)", "url": "https://leetcode.com/problems/coin-change/"},
        ],
        "system_design": [
            "Design Microsoft Teams Real-Time Chat & Video Signaling Server",
            "Design Azure Blob Storage Tiering & Replication Engine",
            "Design Distributed Web Crawler & Indexer",
        ]
    },
    "Meta (Facebook)": {
        "tagline": "Emphasis on High-Speed Execution, Binary Search Variants, & Social Graph Processing",
        "focus_areas": ["Binary Search", "BFS/DFS Social Graph", "Sliding Window", "Speed Coding"],
        "top_questions": [
            {"id": "meta_1", "title": "Kth Largest Element in an Array", "topic": "Quickselect / PriorityQueue", "difficulty": "Medium", "complexity": "Time: O(N) avg, Space: O(1)", "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/"},
            {"id": "meta_2", "title": "Minimum Remove to Make Valid Parentheses", "topic": "Stack / String Building", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(N)", "url": "https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/"},
            {"id": "meta_3", "title": "Product of Array Except Self", "topic": "Prefix & Suffix Products", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(1)", "url": "https://leetcode.com/problems/product-of-array-except-self/"},
            {"id": "meta_4", "title": "Subarray Sum Equals K", "topic": "Prefix Sum + Hash Map", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(N)", "url": "https://leetcode.com/problems/subarray-sum-equals-k/"},
            {"id": "meta_5", "title": "Binary Tree Right Side View", "topic": "Tree / BFS / Level Order", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(D)", "url": "https://leetcode.com/problems/binary-tree-right-side-view/"},
            {"id": "meta_6", "title": "Dot Product of Two Sparse Vectors", "topic": "Two Pointers / Index Pairs", "difficulty": "Medium", "complexity": "Time: O(L1 + L2), Space: O(L)", "url": "https://leetcode.com/problems/dot-product-of-two-sparse-vectors/"},
            {"id": "meta_7", "title": "Range Sum of BST", "topic": "BST Traversal Pruning", "difficulty": "Easy", "complexity": "Time: O(N), Space: O(H)", "url": "https://leetcode.com/problems/range-sum-of-bst/"},
            {"id": "meta_8", "title": "Custom Sort String", "topic": "String Hash Bucket Sort", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(1)", "url": "https://leetcode.com/problems/custom-sort-string/"},
            {"id": "meta_9", "title": "Valid Word Abbreviation", "topic": "Two Pointers Parsing", "difficulty": "Easy", "complexity": "Time: O(N), Space: O(1)", "url": "https://leetcode.com/problems/valid-word-abbreviation/"},
            {"id": "meta_10", "title": "Accounts Merge", "topic": "Union Find / Disjoint Set", "difficulty": "Medium", "complexity": "Time: O(N log N), Space: O(N)", "url": "https://leetcode.com/problems/accounts-merge/"},
        ],
        "system_design": [
            "Design Facebook News Feed Generation & Ranking System",
            "Design Messenger / Real-Time WebSocket Gateway",
            "Design Instagram Story Viewer & Engagement Counter at Scale",
        ]
    },
    "Uber": {
        "tagline": "Emphasis on Geospatial QuadTrees, Real-Time Graph Shortest Paths, & DP",
        "focus_areas": ["Geospatial Indexing (H3/QuadTree)", "Graph Shortest Path", "Dynamic Programming"],
        "top_questions": [
            {"id": "uber_1", "title": "Bus Routes", "topic": "Multi-Source BFS / Graph", "difficulty": "Hard", "complexity": "Time: O(N * S), Space: O(N * S)", "url": "https://leetcode.com/problems/bus-routes/"},
            {"id": "uber_2", "title": "Sliding Window Maximum", "topic": "Monotonic Double Ended Queue", "difficulty": "Hard", "complexity": "Time: O(N), Space: O(K)", "url": "https://leetcode.com/problems/sliding-window-maximum/"},
            {"id": "uber_3", "title": "Sudoku Solver", "topic": "Backtracking / Constraint Check", "difficulty": "Hard", "complexity": "Time: O(9^(9x9)), Space: O(81)", "url": "https://leetcode.com/problems/sudoku-solver/"},
            {"id": "uber_4", "title": "Design Leaderboard", "topic": "Hash Map + TreeMap", "difficulty": "Medium", "complexity": "Time: O(log N), Space: O(N)", "url": "https://leetcode.com/problems/design-a-leaderboard/"},
            {"id": "uber_5", "title": "Shortest Path in Grid with Obstacles Elimination", "topic": "BFS 3D State Search", "difficulty": "Hard", "complexity": "Time: O(M * N * K), Space: O(M * N * K)", "url": "https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/"},
            {"id": "uber_6", "title": "Evaluate Reverse Polish Notation", "topic": "Stack Operand Processing", "difficulty": "Medium", "complexity": "Time: O(N), Space: O(N)", "url": "https://leetcode.com/problems/evaluate-reverse-polish-notation/"},
            {"id": "uber_7", "title": "Target Sum", "topic": "0/1 Knapsack DP", "difficulty": "Medium", "complexity": "Time: O(N * Sum), Space: O(Sum)", "url": "https://leetcode.com/problems/target-sum/"},
        ],
        "system_design": [
            "Design Uber Driver-Rider Matching Engine & Dispatcher",
            "Design Real-Time Driver GPS Location Tracking Pipeline",
            "Design Dynamic Surge Pricing Calculation Engine",
        ]
    }
}

DSA_TOPIC_SHEETS = {
    "1. Arrays & Hashing": [
        {"id": "dsa_1", "name": "Two Sum", "diff": "Easy", "approach": "Use HashMap storing value -> index to find complement (Target - num) in O(N).", "url": "https://leetcode.com/problems/two-sum/"},
        {"id": "dsa_2", "name": "Contains Duplicate", "diff": "Easy", "approach": "Use HashSet to detect duplicate element in single pass O(N).", "url": "https://leetcode.com/problems/contains-duplicate/"},
        {"id": "dsa_3", "name": "Valid Anagram", "diff": "Easy", "approach": "Use character frequency array of size 26 or HashMap to compare counts.", "url": "https://leetcode.com/problems/valid-anagram/"},
        {"id": "dsa_4", "name": "Group Anagrams", "diff": "Medium", "approach": "Categorize strings by sorted key or 26-character tuple frequency map in O(N * L).", "url": "https://leetcode.com/problems/group-anagrams/"},
        {"id": "dsa_5", "name": "Top K Frequent Elements", "diff": "Medium", "approach": "Use Bucket Sort (frequency array) or Min Heap size K to achieve O(N) or O(N log K).", "url": "https://leetcode.com/problems/top-k-frequent-elements/"},
        {"id": "dsa_6", "name": "Product of Array Except Self", "diff": "Medium", "approach": "Precompute Prefix Products pass and Suffix Products pass without division in O(N).", "url": "https://leetcode.com/problems/product-of-array-except-self/"},
        {"id": "dsa_7", "name": "Longest Consecutive Sequence", "diff": "Medium", "approach": "Store numbers in HashSet. Start sequence counting only if (num - 1) is NOT in set O(N).", "url": "https://leetcode.com/problems/longest-consecutive-sequence/"}
    ],
    "2. Two Pointers & Sliding Window": [
        {"id": "dsa_8", "name": "Valid Palindrome", "diff": "Easy", "approach": "Two pointers starting at left and right boundaries moving inward skipping non-alphanumerics.", "url": "https://leetcode.com/problems/valid-palindrome/"},
        {"id": "dsa_9", "name": "3Sum", "diff": "Medium", "approach": "Sort array. Iterate i, then use left/right pointers to find remaining sum with skip duplicates.", "url": "https://leetcode.com/problems/3sum/"},
        {"id": "dsa_10", "name": "Container With Most Water", "diff": "Medium", "approach": "Two pointers at left/right. Compute area, then advance pointer with smaller height.", "url": "https://leetcode.com/problems/container-with-most-water/"},
        {"id": "dsa_11", "name": "Best Time to Buy and Sell Stock", "diff": "Easy", "approach": "Track minimum price seen so far and max profit achieved in single pass O(N).", "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
        {"id": "dsa_12", "name": "Longest Substring Without Repeating Characters", "diff": "Medium", "approach": "Sliding window with HashMap tracking last seen index of each character.", "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
        {"id": "dsa_13", "name": "Longest Repeating Character Replacement", "diff": "Medium", "approach": "Sliding window maintaining max character frequency count in current window.", "url": "https://leetcode.com/problems/longest-repeating-character-replacement/"},
        {"id": "dsa_14", "name": "Minimum Window Substring", "diff": "Hard", "approach": "Sliding window expanding right until all chars found, then shrinking left to minimize length.", "url": "https://leetcode.com/problems/minimum-window-substring/"}
    ],
    "3. Stack & Monotonic Stack": [
        {"id": "dsa_15", "name": "Valid Parentheses", "diff": "Easy", "approach": "Use Stack matching closing brackets with corresponding opening bracket top in O(N).", "url": "https://leetcode.com/problems/valid-parentheses/"},
        {"id": "dsa_16", "name": "Min Stack", "diff": "Medium", "approach": "Maintain auxiliary stack storing minimum element up to current height in O(1).", "url": "https://leetcode.com/problems/min-stack/"},
        {"id": "dsa_17", "name": "Evaluate Reverse Polish Notation", "diff": "Medium", "approach": "Stack operand evaluation popping top 2 elements when operator encountered.", "url": "https://leetcode.com/problems/evaluate-reverse-polish-notation/"},
        {"id": "dsa_18", "name": "Daily Temperatures", "diff": "Medium", "approach": "Monotonic decreasing stack storing indices to find next warmer day in O(N).", "url": "https://leetcode.com/problems/daily-temperatures/"},
        {"id": "dsa_19", "name": "Largest Rectangle in Histogram", "diff": "Hard", "approach": "Monotonic increasing stack tracking height and starting index boundaries in O(N).", "url": "https://leetcode.com/problems/largest-rectangle-in-histogram/"}
    ],
    "4. Binary Search": [
        {"id": "dsa_20", "name": "Binary Search", "diff": "Easy", "approach": "Divide search space in half each iteration using mid = left + (right - left) // 2.", "url": "https://leetcode.com/problems/binary-search/"},
        {"id": "dsa_21", "name": "Search a 2D Matrix", "diff": "Medium", "approach": "Treat 2D grid of size M*N as 1D array using row = mid // N, col = mid % N in O(log M*N).", "url": "https://leetcode.com/problems/search-a-2d-matrix/"},
        {"id": "dsa_22", "name": "Koko Eating Bananas", "diff": "Medium", "approach": "Binary search on speed answer space [1, max(piles)]. Check total hours function.", "url": "https://leetcode.com/problems/koko-eating-bananas/"},
        {"id": "dsa_23", "name": "Find Minimum in Rotated Sorted Array", "diff": "Medium", "approach": "Compare mid with rightmost element. If mid > right, min is in right half; else left half.", "url": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"},
        {"id": "dsa_24", "name": "Search in Rotated Sorted Array", "diff": "Medium", "approach": "Determine which half (left or right) is sorted, then check if target lies within bounds.", "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/"}
    ],
    "5. Linked List": [
        {"id": "dsa_25", "name": "Reverse Linked List", "diff": "Easy", "approach": "Iterative 3-pointer (prev, curr, next) pointer reversal in O(N) time & O(1) space.", "url": "https://leetcode.com/problems/reverse-linked-list/"},
        {"id": "dsa_26", "name": "Merge Two Sorted Lists", "diff": "Easy", "approach": "Iterative dummy node comparison weaving 2 sorted lists in O(N + M).", "url": "https://leetcode.com/problems/merge-two-sorted-lists/"},
        {"id": "dsa_27", "name": "Reorder List", "diff": "Medium", "approach": "Find mid (slow/fast), reverse second half, weave two halves together.", "url": "https://leetcode.com/problems/reorder-list/"},
        {"id": "dsa_28", "name": "Remove Nth Node From End of List", "diff": "Medium", "approach": "Two pointers with N gap fast pointer advancement before moving together.", "url": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/"},
        {"id": "dsa_29", "name": "Linked List Cycle", "diff": "Easy", "approach": "Floyd's Tortoise & Hare algorithm (slow moving 1 step, fast moving 2 steps).", "url": "https://leetcode.com/problems/linked-list-cycle/"}
    ],
    "6. Trees & Tries": [
        {"id": "dsa_30", "name": "Invert Binary Tree", "diff": "Easy", "approach": "Recursive DFS swapping left and right subtrees of each node.", "url": "https://leetcode.com/problems/invert-binary-tree/"},
        {"id": "dsa_31", "name": "Maximum Depth of Binary Tree", "diff": "Easy", "approach": "1 + max(depth(left), depth(right)) using DFS or level order BFS.", "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
        {"id": "dsa_32", "name": "Binary Tree Level Order Traversal", "diff": "Medium", "approach": "Queue BFS processing level by level by measuring queue length at start of loop.", "url": "https://leetcode.com/problems/binary-tree-level-order-traversal/"},
        {"id": "dsa_33", "name": "Validate Binary Search Tree", "diff": "Medium", "approach": "DFS passing min and max allowable bounds for each node.", "url": "https://leetcode.com/problems/validate-binary-search-tree/"},
        {"id": "dsa_34", "name": "Lowest Common Ancestor of BST", "diff": "Medium", "approach": "If both p and q < curr, move left; if both > curr, move right; else curr is LCA.", "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/"},
        {"id": "dsa_35", "name": "Implement Trie (Prefix Tree)", "diff": "Medium", "approach": "TrieNode with children array[26] or dict + isEndOfWord boolean flag.", "url": "https://leetcode.com/problems/implement-trie-prefix-tree/"}
    ],
    "7. Heap / Priority Queue": [
        {"id": "dsa_36", "name": "Kth Largest Element in a Stream", "diff": "Easy", "approach": "Min Heap of capacity K storing top K largest elements seen.", "url": "https://leetcode.com/problems/kth-largest-element-in-a-stream/"},
        {"id": "dsa_37", "name": "Last Stone Weight", "diff": "Easy", "approach": "Max Heap popping top 2 stones, smashing, and pushing remainder until 1 left.", "url": "https://leetcode.com/problems/last-stone-weight/"},
        {"id": "dsa_38", "name": "Task Scheduler", "diff": "Medium", "approach": "Max Heap tracking task frequencies + cooldown Queue.", "url": "https://leetcode.com/problems/task-scheduler/"},
        {"id": "dsa_39", "name": "Find Median from Data Stream", "diff": "Hard", "approach": "Dual Heap (Max Heap for lower half, Min Heap for upper half).", "url": "https://leetcode.com/problems/find-median-from-data-stream/"}
    ],
    "8. Graphs": [
        {"id": "dsa_40", "name": "Number of Islands", "diff": "Medium", "approach": "Grid BFS/DFS marking visited cells to count connected components.", "url": "https://leetcode.com/problems/number-of-islands/"},
        {"id": "dsa_41", "name": "Clone Graph", "diff": "Medium", "approach": "DFS/BFS with HashMap mapping original node -> cloned node to handle cycles.", "url": "https://leetcode.com/problems/clone-graph/"},
        {"id": "dsa_42", "name": "Pacific Atlantic Water Flow", "diff": "Medium", "approach": "Multi-source BFS/DFS from ocean edges inward finding set intersection.", "url": "https://leetcode.com/problems/pacific-atlantic-water-flow/"},
        {"id": "dsa_43", "name": "Course Schedule (Topological Sort)", "diff": "Medium", "approach": "Calculate indegrees. Push zero-indegree nodes to queue (Kahn's BFS Algorithm).", "url": "https://leetcode.com/problems/course-schedule/"}
    ],
    "9. Dynamic Programming": [
        {"id": "dsa_44", "name": "Climbing Stairs", "diff": "Easy", "approach": "Fibonacci transition dp[i] = dp[i-1] + dp[i-2] optimized to O(1) space.", "url": "https://leetcode.com/problems/climbing-stairs/"},
        {"id": "dsa_45", "name": "House Robber", "diff": "Medium", "approach": "dp[i] = max(dp[i-1], dp[i-2] + nums[i]) tracking current max profit.", "url": "https://leetcode.com/problems/house-robber/"},
        {"id": "dsa_46", "name": "Coin Change", "diff": "Medium", "approach": "Unbounded knapsack DP: dp[i] = min(dp[i], 1 + dp[i - coin]) initialized to infinity.", "url": "https://leetcode.com/problems/coin-change/"},
        {"id": "dsa_47", "name": "Longest Increasing Subsequence", "diff": "Medium", "approach": "O(N^2) DP or O(N log N) using Binary Search on active tail lists.", "url": "https://leetcode.com/problems/longest-increasing-subsequence/"},
        {"id": "dsa_48", "name": "Edit Distance", "diff": "Hard", "approach": "2D DP grid comparing insert, delete, and replace operational choices.", "url": "https://leetcode.com/problems/edit-distance/"}
    ]
}

CORE_CS_SUBJECTS = {
    "DBMS & SQL": [
        {"id": "db_1", "q": "Difference between SQL (Relational) and NoSQL databases?", "a": "Relational DBs (PostgreSQL, MySQL) use structured schemas, SQL, and strict ACID transactions (ideal for finance/CRM). NoSQL (MongoDB, DynamoDB) offers horizontal scaling, flexible document/key-value schemas, and BASE eventual consistency."},
        {"id": "db_2", "q": "What are Database Indexes and how do B+ Trees work?", "a": "Indexes speed up SELECT queries from O(N) full table scans to O(log N) using self-balancing B+ Trees. B+ Tree leaf nodes are linked sequentially for fast range scans. Indexes increase disk usage and slow down INSERT/UPDATE/DELETE."},
        {"id": "db_3", "q": "What are ACID Properties in Relational Databases?", "a": "Atomicity (all operations commit or all roll back), Consistency (data follows constraint rules), Isolation (concurrent transactions don't interfere via locking/MVCC), and Durability (committed data persists across server crashes)."},
        {"id": "db_4", "q": "What is Database Sharding vs Vertical Partitioning?", "a": "Horizontal Sharding splits database rows across multiple servers by Shard Key (e.g. user_id % 4). Vertical Partitioning splits columns across different tables or servers (e.g. Core profile vs Blob media data)."}
    ],
    "Operating Systems": [
        {"id": "os_1", "q": "Difference between Process and Thread?", "a": "A Process is an executing instance with its own isolated virtual memory space. A Thread is a lightweight unit of execution within a process that shares memory and heap with sibling threads, reducing context switch overhead."},
        {"id": "os_2", "q": "What is Deadlock and what are Coffman's 4 Conditions?", "a": "Deadlock occurs when processes wait indefinitely for resources held by each other. Conditions: 1) Mutual Exclusion, 2) Hold and Wait, 3) No Preemption, 4) Circular Wait. Solved using Banker's Algorithm or ordering resource allocation."},
        {"id": "os_3", "q": "What is Virtual Memory, Paging, and Page Faults?", "a": "Virtual Memory maps process addresses to physical RAM using fixed-size Paging. If requested page isn't in RAM, hardware triggers a Page Fault interrupt to fetch page from swap disk using OS Page Replacement algorithms (LRU, FIFO)."},
        {"id": "os_4", "q": "Mutex vs Semaphore?", "a": "Mutex is a locking mechanism (ownership by 1 thread at a time). Semaphore is a signaling mechanism (counter allowing up to N threads access concurrently)."}
    ],
    "System Design": [
        {"id": "sys_1", "q": "How to scale a web app from 1K to 1M daily active users?", "a": "1) Decouple Web & DB. 2) Add Load Balancers + Stateless Web Servers. 3) Implement Redis/Memcached Caching layer. 4) Use CDN for static media. 5) DB Read Replicas & Horizontal Sharding. 6) Asynchronous Message Queues (Kafka/RabbitMQ)."},
        {"id": "sys_2", "q": "Explain Consistent Hashing and why it's critical for distributed caches?", "a": "Consistent Hashing maps servers and keys onto a 360° hash ring. When a server is added or removed, only k/N keys need remapping rather than re-hashing all keys, avoiding cache stampedes in Redis/Memcached clusters."},
        {"id": "sys_3", "q": "What is CAP Theorem?", "a": "In a distributed system during Network Partitions (P), you can only guarantee Consistency (C - all nodes see exact same data) OR Availability (A - every request receives non-error response), but not both simultaneously (CP vs AP)."},
        {"id": "sys_4", "q": "Rate Limiting Algorithms (Token Bucket vs Leaky Bucket vs Fixed Window)?", "a": "Token Bucket adds tokens at a fixed rate (allows burst traffic). Leaky Bucket processes requests at a constant smooth rate. Fixed Window resets count per interval (vulnerable to burst spikes at boundary limits)."}
    ],
    "Computer Networks": [
        {"id": "net_1", "q": "Difference between TCP and UDP?", "a": "TCP is connection-oriented, reliable, guarantees packet order using 3-Way Handshake & acknowledgments (used in HTTP/HTTPS, DB, SSH). UDP is connectionless, fast, has zero handshake overhead, but allows packet loss (used in Video Streaming, VoIP, Gaming)."},
        {"id": "net_2", "q": "What happens when you enter 'https://google.com' in browser?", "a": "1) Browser & OS DNS Cache lookup ➔ 2) Recursive DNS Resolver ➔ 3) TCP 3-Way Handshake (SYN, SYN-ACK, ACK) ➔ 4) TLS/SSL Handshake & Certificate Verification ➔ 5) HTTP GET Request ➔ 6) Server/CDN Response ➔ 7) Browser DOM/CSSOM Rendering."},
        {"id": "net_3", "q": "What is WebSockets vs HTTP Long Polling?", "a": "HTTP Long Polling keeps request open until server has new data, then client reconnects. WebSockets establish a full-duplex, persistent bidirectional TCP connection for instant real-time events with minimal header overhead."}
    ]
}
