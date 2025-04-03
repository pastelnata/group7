class Node:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

class BookBST:
    def __init__(self, key):
        self.root = None
        self.key = key
    
    def insert(self, book):
        """Insert a book into the BST"""
        if not self.root:
            self.root = Node(book)
            return
        
        current = self.root
        while True:
            book_key = getattr(book, self.key).lower()
            current_key = getattr(current.book, self.key).lower()
            if book_key < current_key:
                if current.left is None:
                    current.left = Node(book)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(book)
                    break
                current = current.right
    
    def search(self, query, limit=25):
        """Search for books with titles containing the query"""
        query = query.lower()
        results = []
        
        def inorder_search(node):
            if not node or len(results) >= limit:
                return
            
            # Traverse left subtree
            inorder_search(node.left)
            
            # Process current node
            book_key = getattr(node.book, self.key).lower()
            if len(results) < limit and query in book_key:
                results.append(node.book)
            
            # Traverse right subtree
            inorder_search(node.right)
        
        inorder_search(self.root)
        return results
    
    def build_from_queryset(self, queryset):
        """Build a balanced BST from a Django queryset of books"""
        sorted_books = sorted(queryset, key=lambda book: getattr(book, self.key).lower())

        def build_balanced_tree(books):
            if not books:
                return None
            
            # Find the middle element
            mid = len(books) // 2
            root = Node(books[mid])
            
            # Recursively build left and right subtrees
            root.left = build_balanced_tree(books[:mid])
            root.right = build_balanced_tree(books[mid + 1:])
            
            return root

        self.root = build_balanced_tree(sorted_books)