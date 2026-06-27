#!/bin/bash
# Setup disposable Frappe bench for vietnam_compliance testing
# Usage: ./scripts/setup_bench.sh
set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "Prerequisites: brew install mariadb@11.8 redis"
echo "Bench will be at: $REPO_ROOT/bench"
echo ""

# Start services
brew services start mariadb@11.8 2>/dev/null || true
redis-server --port 11000 --daemonize yes 2>/dev/null || true
redis-server --port 13000 --daemonize yes 2>/dev/null || true
sleep 1

# Set MariaDB password
/opt/homebrew/opt/mariadb@11.8/bin/mariadb -u $(whoami) -e "ALTER USER '$(whoami)'@'localhost' IDENTIFIED BY 'password'; FLUSH PRIVILEGES;" 2>/dev/null || true

# Init bench
if [ ! -d "bench" ]; then
    bench init bench --frappe-branch version-16 --python $(which python3)
fi

cd bench
bench set-config -g mariadb_root_password password 2>/dev/null || true
bench set-config -g mariadb_root_username $(whoami) 2>/dev/null || true

# Get apps
bench get-app erpnext --branch version-16 2>/dev/null || echo "ERPNext OK"

# Create site
bench list-sites 2>/dev/null | grep -q test.local || \
    bench new-site test.local --db-name test_local --admin-password admin \
        --db-root-username $(whoami) --db-root-password password --force

# Install apps
bench --site test.local install-app erpnext 2>/dev/null || echo "ERPNext installed"
bench --site test.local uninstall-app vietnam_compliance --yes 2>/dev/null || true

# Sync app code
rsync -a "$REPO_ROOT/vietnam_compliance/" apps/vietnam_compliance/vietnam_compliance/
bench build --app vietnam_compliance
bench --site test.local install-app vietnam_compliance

echo ""
bench --site test.local list-apps
echo ""
echo "=== Dev server: cd bench && bench start"
