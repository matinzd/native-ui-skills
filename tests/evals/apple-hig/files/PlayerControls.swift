import SwiftUI

struct PlayerControls: View {
    @State private var isPlaying = false
    @State private var pulse = false
    let track: Track

    var body: some View {
        VStack(spacing: 8) {
            Image("album-sparkle-overlay")
            Text(track.title).font(.headline)
            Text(track.artist)
                .font(.caption)
                .foregroundStyle(Color(white: 0.8))
            HStack(spacing: 4) {
                Image(systemName: "backward.fill").frame(width: 20, height: 20)
                    .onTapGesture { Player.shared.previous() }
                Image(systemName: isPlaying ? "pause.fill" : "play.fill").frame(width: 20, height: 20)
                    .scaleEffect(pulse ? 1.3 : 1.0)
                    .onTapGesture { isPlaying.toggle() }
                Image(systemName: "forward.fill").frame(width: 20, height: 20)
                    .onTapGesture { Player.shared.next() }
            }
        }
        .background(Color.white)
        .dynamicTypeSize(.medium)
        .onAppear {
            withAnimation(.easeInOut(duration: 0.4).repeatForever()) { pulse = true }
        }
    }
}
