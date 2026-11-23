import SwiftUI

struct RootTabs: View {
    @State private var selected = 0
    private let icons = ["house", "magnifyingglass", "heart", "cart", "bell", "person", "gearshape"]

    var body: some View {
        VStack(spacing: 0) {
            ScreenFactory.screen(at: selected)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            HStack(spacing: 0) {
                ForEach(icons.indices, id: \.self) { i in
                    Image(systemName: icons[i])
                        .font(.system(size: 18))
                        .foregroundColor(selected == i ? .blue : .gray)
                        .frame(maxWidth: .infinity)
                        .onTapGesture { selected = i }
                }
            }
            .frame(height: 40)
            .background(Color.white)
        }
    }
}
