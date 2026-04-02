"""
AI Mock Interview Engine Backend Module
Handles interview question generation, evaluation, and scoring
"""

import google.generativeai as genai
import os
from datetime import datetime
import json


class InterviewEngine:
    """
    AI-powered interview engine for conducting mock interviews
    Supports multiple topics and difficulty levels
    """
    
    def __init__(self):
        """Initialize the interview engine with Gemini API"""
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY', '')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def get_questions(self, topic, difficulty, num_questions=5):
        """
        Generate interview questions based on topic and difficulty
        
        Args:
            topic (str): Interview topic (Python, DSA, Web Development, DBMS)
            difficulty (str): Difficulty level (Easy, Medium, Hard)
            num_questions (int): Number of questions to generate
        
        Returns:
            list: List of question dictionaries
        """
        
        # Predefined question bank for reliability
        question_bank = {
            "Python": {
                "Easy": [
                    {
                        "question": "What are the key differences between lists and tuples in Python?",
                        "hint": "Think about mutability and use cases",
                        "expected_points": ["mutability", "immutable", "performance", "syntax", "use cases"]
                    },
                    {
                        "question": "Explain what Python decorators are and provide a simple example.",
                        "hint": "Decorators modify or enhance functions",
                        "expected_points": ["function wrapper", "@syntax", "higher-order function", "example"]
                    },
                    {
                        "question": "What is the difference between '==' and 'is' operators in Python?",
                        "hint": "Think about value comparison vs identity comparison",
                        "expected_points": ["value equality", "identity", "memory address", "is checks same object"]
                    },
                    {
                        "question": "How does list comprehension work in Python? Give an example.",
                        "hint": "It's a concise way to create lists",
                        "expected_points": ["syntax", "example", "efficient", "readable"]
                    },
                    {
                        "question": "What are *args and **kwargs in Python functions?",
                        "hint": "They allow variable number of arguments",
                        "expected_points": ["variable arguments", "*args for positional", "**kwargs for keyword", "unpacking"]
                    }
                ],
                "Medium": [
                    {
                        "question": "Explain the concept of generators in Python and why they are memory efficient.",
                        "hint": "They use yield instead of return",
                        "expected_points": ["yield", "lazy evaluation", "memory efficient", "iterator", "one value at a time"]
                    },
                    {
                        "question": "What is the Global Interpreter Lock (GIL) in Python and how does it affect multithreading?",
                        "hint": "It's a mutex that protects Python objects",
                        "expected_points": ["mutex", "single thread execution", "CPython", "performance impact", "multiprocessing alternative"]
                    },
                    {
                        "question": "Explain context managers in Python and implement a custom one using __enter__ and __exit__.",
                        "hint": "Used with 'with' statement",
                        "expected_points": ["with statement", "__enter__", "__exit__", "resource management", "example"]
                    },
                    {
                        "question": "What are metaclasses in Python? When would you use them?",
                        "hint": "Classes of classes",
                        "expected_points": ["class creation", "type", "advanced feature", "use cases", "class factory"]
                    },
                    {
                        "question": "Explain the difference between deepcopy and shallow copy in Python.",
                        "hint": "Think about nested objects",
                        "expected_points": ["copy module", "nested objects", "independent copy", "reference", "mutable objects"]
                    }
                ],
                "Hard": [
                    {
                        "question": "Explain Python's memory management and garbage collection mechanism in detail.",
                        "hint": "Reference counting and generational garbage collection",
                        "expected_points": ["reference counting", "garbage collector", "circular references", "generations", "gc module"]
                    },
                    {
                        "question": "What are descriptors in Python? Implement a custom descriptor class.",
                        "hint": "They define __get__, __set__, __delete__",
                        "expected_points": ["__get__", "__set__", "__delete__", "property", "implementation example"]
                    },
                    {
                        "question": "Explain the asyncio framework and how async/await works in Python.",
                        "hint": "Event loop and coroutines",
                        "expected_points": ["event loop", "coroutines", "async/await", "concurrency", "I/O operations"]
                    },
                    {
                        "question": "How would you optimize Python code for performance? Discuss various techniques.",
                        "hint": "Multiple approaches from algorithm to implementation",
                        "expected_points": ["profiling", "algorithm optimization", "built-in functions", "Cython", "vectorization", "caching"]
                    },
                    {
                        "question": "Explain method resolution order (MRO) in Python's multiple inheritance.",
                        "hint": "C3 linearization algorithm",
                        "expected_points": ["MRO", "C3 linearization", "diamond problem", "__mro__", "super()"]
                    }
                ]
            },
            "DSA": {
                "Easy": [
                    {
                        "question": "Explain the difference between arrays and linked lists. What are their time complexities?",
                        "hint": "Consider access, insertion, and deletion operations",
                        "expected_points": ["contiguous memory", "random access", "O(1) access for arrays", "O(n) for linked list", "insertion/deletion"]
                    },
                    {
                        "question": "What is a stack? Explain with real-world examples and implement push/pop operations.",
                        "hint": "Last In First Out (LIFO)",
                        "expected_points": ["LIFO", "push", "pop", "real-world examples", "implementation"]
                    },
                    {
                        "question": "Explain binary search algorithm and its time complexity.",
                        "hint": "Works on sorted arrays",
                        "expected_points": ["sorted array", "divide and conquer", "O(log n)", "implementation", "conditions"]
                    },
                    {
                        "question": "What is the difference between BFS and DFS? When would you use each?",
                        "hint": "Breadth-First vs Depth-First",
                        "expected_points": ["BFS uses queue", "DFS uses stack", "level-order vs depth", "use cases", "completeness"]
                    },
                    {
                        "question": "Explain time complexity using Big O notation with examples.",
                        "hint": "Describes how runtime grows",
                        "expected_points": ["Big O notation", "O(1), O(n), O(log n)", "worst case", "examples", "growth rate"]
                    }
                ],
                "Medium": [
                    {
                        "question": "Explain different tree traversal methods (inorder, preorder, postorder) with examples.",
                        "hint": "Different orders of visiting nodes",
                        "expected_points": ["inorder", "preorder", "postorder", "recursive", "examples", "applications"]
                    },
                    {
                        "question": "What is dynamic programming? Explain with the example of Fibonacci sequence.",
                        "hint": "Optimal substructure and overlapping subproblems",
                        "expected_points": ["memoization", "tabulation", "overlapping subproblems", "Fibonacci example", "optimization"]
                    },
                    {
                        "question": "Explain how hash tables work. How do you handle collisions?",
                        "hint": "Key-value pairs with O(1) average lookup",
                        "expected_points": ["hash function", "collision handling", "chaining", "open addressing", "O(1) average case"]
                    },
                    {
                        "question": "What is a binary search tree? Explain insertion and searching operations.",
                        "hint": "Left child < parent < right child",
                        "expected_points": ["BST property", "insertion process", "search operation", "time complexity", "balanced vs unbalanced"]
                    },
                    {
                        "question": "Explain the concept of heaps. What are min-heap and max-heap?",
                        "hint": "Complete binary tree with heap property",
                        "expected_points": ["heap property", "min-heap", "max-heap", "heapify", "priority queue"]
                    }
                ],
                "Hard": [
                    {
                        "question": "Explain different graph algorithms: Dijkstra's, Bellman-Ford, and Floyd-Warshall.",
                        "hint": "Shortest path algorithms",
                        "expected_points": ["shortest path", "Dijkstra's", "Bellman-Ford", "Floyd-Warshall", "use cases", "complexity"]
                    },
                    {
                        "question": "What are AVL trees and Red-Black trees? How do they maintain balance?",
                        "hint": "Self-balancing binary search trees",
                        "expected_points": ["AVL balance factor", "rotations", "Red-Black properties", "O(log n) operations", "comparison"]
                    },
                    {
                        "question": "Explain the A* algorithm and its heuristic function. How is it different from Dijkstra's?",
                        "hint": "Informed search algorithm",
                        "expected_points": ["heuristic function", "f(n) = g(n) + h(n)", "admissible heuristic", "pathfinding", "vs Dijkstra"]
                    },
                    {
                        "question": "What is a Trie data structure? Implement insert and search operations.",
                        "hint": "Prefix tree for string operations",
                        "expected_points": ["prefix tree", "string storage", "insert operation", "search operation", "applications", "space complexity"]
                    },
                    {
                        "question": "Explain segment trees and their applications. How do you build and query them?",
                        "hint": "Range query data structure",
                        "expected_points": ["range queries", "build process", "query operation", "update operation", "applications", "time complexity"]
                    }
                ]
            },
            "Web Development": {
                "Easy": [
                    {
                        "question": "What is the difference between GET and POST HTTP methods?",
                        "hint": "Think about data transmission and use cases",
                        "expected_points": ["GET retrieves data", "POST sends data", "URL parameters", "security", "idempotent"]
                    },
                    {
                        "question": "Explain the CSS box model with all its components.",
                        "hint": "Content, padding, border, margin",
                        "expected_points": ["content", "padding", "border", "margin", "box-sizing"]
                    },
                    {
                        "question": "What is the Document Object Model (DOM)? How do you manipulate it?",
                        "hint": "Tree structure of HTML",
                        "expected_points": ["tree structure", "nodes", "manipulation methods", "getElementById", "querySelector"]
                    },
                    {
                        "question": "Explain the difference between == and === in JavaScript.",
                        "hint": "Type coercion vs strict equality",
                        "expected_points": ["type coercion", "strict equality", "type checking", "examples"]
                    },
                    {
                        "question": "What are semantic HTML tags? Give examples and explain their importance.",
                        "hint": "Meaningful tags like header, article, section",
                        "expected_points": ["semantic meaning", "examples", "accessibility", "SEO", "code readability"]
                    }
                ],
                "Medium": [
                    {
                        "question": "Explain how promises work in JavaScript. What is async/await?",
                        "hint": "Handling asynchronous operations",
                        "expected_points": ["asynchronous", "then/catch", "promise states", "async/await", "error handling"]
                    },
                    {
                        "question": "What is CORS? Why is it important and how do you handle it?",
                        "hint": "Cross-Origin Resource Sharing",
                        "expected_points": ["cross-origin", "security", "CORS headers", "preflight request", "handling methods"]
                    },
                    {
                        "question": "Explain the concept of RESTful APIs. What are the best practices?",
                        "hint": "Representational State Transfer",
                        "expected_points": ["REST principles", "HTTP methods", "stateless", "resource-based", "best practices"]
                    },
                    {
                        "question": "What is the Virtual DOM in React? How does it improve performance?",
                        "hint": "Efficient DOM updates",
                        "expected_points": ["Virtual DOM", "diffing algorithm", "reconciliation", "performance", "real DOM comparison"]
                    },
                    {
                        "question": "Explain event bubbling and event capturing in JavaScript.",
                        "hint": "Event propagation phases",
                        "expected_points": ["bubbling", "capturing", "propagation", "stopPropagation", "event delegation"]
                    }
                ],
                "Hard": [
                    {
                        "question": "Explain the event loop in JavaScript. How does it handle asynchronous operations?",
                        "hint": "Call stack, callback queue, microtask queue",
                        "expected_points": ["call stack", "event loop", "callback queue", "microtasks", "macrotasks", "execution order"]
                    },
                    {
                        "question": "What are service workers? How do they enable Progressive Web Apps?",
                        "hint": "Background scripts for PWAs",
                        "expected_points": ["background script", "caching", "offline support", "lifecycle", "PWA features"]
                    },
                    {
                        "question": "Explain different web security vulnerabilities (XSS, CSRF, SQL Injection) and prevention.",
                        "hint": "Common web security threats",
                        "expected_points": ["XSS", "CSRF", "SQL Injection", "prevention methods", "sanitization", "tokens"]
                    },
                    {
                        "question": "What is server-side rendering (SSR) vs client-side rendering (CSR)? Compare their pros and cons.",
                        "hint": "Where the HTML is generated",
                        "expected_points": ["SSR", "CSR", "performance", "SEO", "initial load", "pros and cons"]
                    },
                    {
                        "question": "Explain WebSockets. How are they different from HTTP? When would you use them?",
                        "hint": "Full-duplex communication",
                        "expected_points": ["bidirectional", "persistent connection", "vs HTTP", "real-time", "use cases"]
                    }
                ]
            },
            "DBMS": {
                "Easy": [
                    {
                        "question": "What is the difference between SQL and NoSQL databases? Give examples of each.",
                        "hint": "Relational vs Non-relational",
                        "expected_points": ["SQL relational", "NoSQL types", "schema", "examples", "use cases"]
                    },
                    {
                        "question": "Explain the ACID properties in database transactions.",
                        "hint": "Atomicity, Consistency, Isolation, Durability",
                        "expected_points": ["Atomicity", "Consistency", "Isolation", "Durability", "examples"]
                    },
                    {
                        "question": "What is a primary key? How is it different from a foreign key?",
                        "hint": "Unique identifier vs reference",
                        "expected_points": ["primary key unique", "foreign key reference", "relationships", "constraints"]
                    },
                    {
                        "question": "Explain the different types of SQL JOINs with examples.",
                        "hint": "INNER, LEFT, RIGHT, FULL",
                        "expected_points": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "examples"]
                    },
                    {
                        "question": "What is normalization? Explain the First Normal Form (1NF).",
                        "hint": "Organizing data to reduce redundancy",
                        "expected_points": ["reduce redundancy", "1NF rules", "atomic values", "benefits"]
                    }
                ],
                "Medium": [
                    {
                        "question": "Explain database normalization up to 3NF. Why is it important?",
                        "hint": "1NF, 2NF, 3NF rules",
                        "expected_points": ["1NF", "2NF", "3NF", "dependencies", "redundancy reduction", "anomalies"]
                    },
                    {
                        "question": "What are database indexes? How do they improve query performance?",
                        "hint": "Data structure for fast lookups",
                        "expected_points": ["B-tree", "fast lookup", "performance", "trade-offs", "types of indexes"]
                    },
                    {
                        "question": "Explain the difference between clustered and non-clustered indexes.",
                        "hint": "Physical ordering of data",
                        "expected_points": ["clustered ordering", "non-clustered pointer", "one per table", "performance", "use cases"]
                    },
                    {
                        "question": "What is a database transaction? Explain transaction isolation levels.",
                        "hint": "Unit of work with ACID properties",
                        "expected_points": ["transaction", "isolation levels", "Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"]
                    },
                    {
                        "question": "Explain stored procedures and triggers. When would you use them?",
                        "hint": "Reusable code in database",
                        "expected_points": ["stored procedures", "triggers", "advantages", "use cases", "examples"]
                    }
                ],
                "Hard": [
                    {
                        "question": "Explain database sharding and partitioning. How do they scale databases?",
                        "hint": "Horizontal and vertical scaling",
                        "expected_points": ["sharding", "partitioning", "horizontal vs vertical", "scaling", "challenges"]
                    },
                    {
                        "question": "What is the CAP theorem? Explain with examples of different databases.",
                        "hint": "Consistency, Availability, Partition tolerance",
                        "expected_points": ["CAP theorem", "trade-offs", "examples", "distributed systems", "consistency models"]
                    },
                    {
                        "question": "Explain MVCC (Multi-Version Concurrency Control) and how it handles concurrent transactions.",
                        "hint": "Multiple versions of data",
                        "expected_points": ["MVCC", "snapshots", "concurrency", "no locks on reads", "PostgreSQL example"]
                    },
                    {
                        "question": "What are database replication strategies? Explain master-slave and master-master replication.",
                        "hint": "Data synchronization across servers",
                        "expected_points": ["replication", "master-slave", "master-master", "consistency", "use cases", "challenges"]
                    },
                    {
                        "question": "Explain query optimization techniques. How does the query optimizer work?",
                        "hint": "Execution plans and cost estimation",
                        "expected_points": ["query optimizer", "execution plan", "cost estimation", "optimization techniques", "EXPLAIN", "statistics"]
                    }
                ]
            }
        }
        
        # Get questions from the bank
        if topic in question_bank and difficulty in question_bank[topic]:
            questions = question_bank[topic][difficulty][:num_questions]
            return questions
        
        return []
    
    def evaluate_answer(self, question, user_answer, expected_points):
        """
        Evaluate user's answer using AI
        
        Args:
            question (str): The interview question
            user_answer (str): User's answer
            expected_points (list): Key points expected in the answer
        
        Returns:
            dict: Evaluation result with score, feedback, and strengths/weaknesses
        """
        
        if not self.model or not user_answer.strip():
            return {
                "score": 0,
                "feedback": "Please provide an answer.",
                "strengths": [],
                "weaknesses": ["No answer provided"],
                "improvement": "Please attempt to answer the question."
            }
        
        try:
            # Create evaluation prompt
            prompt = f"""You are an expert technical interviewer evaluating a candidate's answer.

Question: {question}

Expected Key Points: {', '.join(expected_points)}

Candidate's Answer: {user_answer}

Evaluate this answer and provide:
1. Score out of 10 (be fair but strict)
2. Brief feedback (2-3 sentences)
3. Strengths (what they did well)
4. Weaknesses (what they missed or got wrong)
5. Improvement suggestions

Format your response as JSON:
{{
    "score": <number 0-10>,
    "feedback": "<feedback text>",
    "strengths": ["<strength1>", "<strength2>"],
    "weaknesses": ["<weakness1>", "<weakness2>"],
    "improvement": "<improvement suggestion>"
}}"""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Try to extract JSON from the response
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON response
            evaluation = json.loads(result_text)
            
            return evaluation
            
        except Exception as e:
            # Fallback evaluation based on keyword matching
            score = 0
            matched_points = []
            missed_points = []
            
            answer_lower = user_answer.lower()
            for point in expected_points:
                if point.lower() in answer_lower:
                    score += 2
                    matched_points.append(point)
                else:
                    missed_points.append(point)
            
            score = min(score, 10)
            
            return {
                "score": score,
                "feedback": f"Your answer scored {score}/10. Try to cover more key concepts mentioned in the expected points.",
                "strengths": matched_points if matched_points else ["Attempted the question"],
                "weaknesses": missed_points if missed_points else ["Could be more detailed"],
                "improvement": "Include more technical details and cover the key concepts comprehensively."
            }
    
    def generate_final_report(self, results):
        """
        Generate comprehensive interview report
        
        Args:
            results (list): List of evaluation results for all questions
        
        Returns:
            dict: Complete interview report with analysis
        """
        
        total_score = sum(r['score'] for r in results)
        max_score = len(results) * 10
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Aggregate strengths and weaknesses
        all_strengths = []
        all_weaknesses = []
        
        for result in results:
            all_strengths.extend(result.get('strengths', []))
            all_weaknesses.extend(result.get('weaknesses', []))
        
        # Determine performance level
        if percentage >= 80:
            performance = "Excellent"
            remarks = "Outstanding performance! You demonstrated strong understanding of the concepts."
        elif percentage >= 60:
            performance = "Good"
            remarks = "Good job! You have a solid grasp of the fundamentals. Keep practicing to master advanced concepts."
        elif percentage >= 40:
            performance = "Average"
            remarks = "Average performance. Focus on understanding core concepts better and practice more."
        else:
            performance = "Needs Improvement"
            remarks = "You need more practice. Review the fundamentals and try again."
        
        report = {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "performance": performance,
            "remarks": remarks,
            "top_strengths": list(set(all_strengths))[:5] if all_strengths else ["Completed the interview"],
            "areas_to_improve": list(set(all_weaknesses))[:5] if all_weaknesses else ["Practice more technical concepts"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return report


# Convenience functions for easy import
def get_interview_questions(topic, difficulty, num_questions=5):
    """Get interview questions for a topic and difficulty"""
    engine = InterviewEngine()
    return engine.get_questions(topic, difficulty, num_questions)


def evaluate_interview_answer(question, user_answer, expected_points):
    """Evaluate a single answer"""
    engine = InterviewEngine()
    return engine.evaluate_answer(question, user_answer, expected_points)


def create_interview_report(results):
    """Create final interview report"""
    engine = InterviewEngine()
    return engine.generate_final_report(results)
