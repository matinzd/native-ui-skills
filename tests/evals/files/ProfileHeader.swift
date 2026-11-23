import SwiftUI

struct ProfileHeader: View {
    let user: User
    var onEdit: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(user.name).font(.system(size: 24, weight: .semibold))
            Text(user.handle)
                .font(.system(size: 14))
                .foregroundColor(.secondary)
            Text(user.bio).font(.system(size: 14)).lineLimit(2)
            Button("Edit Profile", action: onEdit)
                .buttonStyle(.bordered)
        }
        .padding()
    }
}
