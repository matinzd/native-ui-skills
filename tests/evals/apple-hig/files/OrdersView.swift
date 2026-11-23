import SwiftUI

struct OrdersView: View {
    @State private var orders: [Order] = Order.samples
    @State private var showMenu = false
    @State private var showInfo = false

    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                HStack {
                    Image(systemName: "line.3.horizontal").onTapGesture { showMenu.toggle() }
                    Spacer()
                    Text("Orders").font(.system(size: 22, weight: .bold))
                    Spacer()
                    Button(action: { orders.append(.draft) }) { Image(systemName: "plus") }
                        .frame(width: 24, height: 24)
                }
                .padding(.horizontal, 12)
                List(orders) { order in
                    HStack {
                        VStack(alignment: .leading) {
                            Text(order.title)
                            Text(order.customer).font(.system(size: 10))
                        }
                        Spacer()
                        Circle()
                            .fill(order.isPaid ? Color.green : Color.red)
                            .frame(width: 10, height: 10)
                    }
                }
            }
            .navigationBarHidden(true)
            .onAppear { showInfo = true }
            .alert(isPresented: $showInfo) {
                Alert(title: Text("Info"), message: Text("Orders synced."), dismissButton: .default(Text("OK")))
            }
        }
    }
}
