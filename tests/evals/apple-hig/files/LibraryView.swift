import SwiftUI

struct LibraryView: View {
    @State private var books: [Book] = Book.samples
    private var isPad: Bool { UIDevice.current.userInterfaceIdiom == .pad }

    var body: some View {
        NavigationStack {
            List(books) { book in
                NavigationLink(book.title) { BookDetail(book: book) }
                    .font(.system(size: isPad ? 22 : 16))
            }
            .padding(.horizontal, isPad ? 200 : 0)
            .navigationTitle("Library")
        }
    }
}
