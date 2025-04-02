from .views import search_books

def run_search_interface():
    """Run interactive book search system"""
    print("Welcome to the Book Search System")
    print("=" * 80)
    
    while True:
        print("\nMain Menu:")
        print("1. Search Books")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == '1':
            search_interface()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    print("\nThank you for using the Book Search System!")

def search_interface():
    """Interactive book search interface"""
    while True:
        print("\nBook Search")
        print("-" * 80)
        print("Enter your search query (or 'q' to quit):")
        
        # Wait for user input
        query = input("> ").strip()
        
        # Check if user wants to quit
        if query.lower() == 'q':
            break
        
        if not query:
            print("Please enter a search term.")
            continue
        
        results = search_books(query)
        print(f"\nSearch results for '{query}' ({len(results)} results):")
        
        for i, book in enumerate(results, 1):
            print(f"\n{i}. {book.title}")
            print(f"   Author: {book.author}")
            print(f"   Rating: {book.stars} stars")
            print(f"   Price: ${book.price}")
            print(f"   Category: {book.category_name}")
        
        print("\nPress Enter to continue...")
        input()

if __name__ == "__main__":
    run_search_interface() 