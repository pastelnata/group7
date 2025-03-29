class Node:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

class BookBST:
    def __init__(self):
        self.root = None
    
    def insert(self, book):
        """Insert a book into the BST"""
        if not self.root:
            self.root = Node(book)
            return
        
        current = self.root
        while True:
            if book.title.lower() < current.book.title.lower():
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
            if len(results) < limit and query in node.book.title.lower():
                results.append(node.book)
            
            # Traverse right subtree
            inorder_search(node.right)
        
        inorder_search(self.root)
        return results
    
    def build_from_queryset(self, queryset):
        """Build BST from a Django queryset of books"""
        for book in queryset:
            self.insert(book) 