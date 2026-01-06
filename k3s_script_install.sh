# 1. Definim variabilele (Copy-Paste la tot blocul)
K3S_TOKEN="K109f2f3ddd86f746541677632810a8c0ed9d7d1be8922a03c01d293381e3bb66b5::server:66812349bc29281b76a11a64ec616671"
K3S_URL="https://192.168.0.172:6443"

# 2. Rulăm instalarea cu flag-ul -t
for node in worker-1 worker-2 worker-3; do
  echo "--- Retry Installing on $node ---"
  # Atentie la -t pus imediat dupa ssh
  ssh -t $node "curl -sfL https://get.k3s.io | K3S_URL=$K3S_URL K3S_TOKEN=$K3S_TOKEN sh -"
done
