// Accepted, but g++ -Wall warns: an unused variable and a variable that may be used uninitialized.
#include <bits/stdc++.h>
using namespace std;

int32_t main() {
    cin.tie(0); ios::sync_with_stdio(0);
    int a, b, unused;
    int maybe;
    cin >> a >> b;
    if (b > 100) maybe = b;
    if (b > 2000000) b = maybe;
    vector<bool> prime(b + 1, true);
    prime[0] = false;
    if (b >= 1) prime[1] = false;
    for (int i = 2; (long long)i * i <= b; i++)
        if (prime[i])
            for (int j = i * i; j <= b; j += i) prime[j] = false;
    int cnt = 0, lo = -1, hi = -1;
    for (int x = a; x <= b; x++) {
        if (!prime[x]) continue;
        cnt++;
        if (lo == -1) lo = x;
        hi = x;
    }
    cout << cnt << '\n';
    if (cnt == 0) cout << "-\n";
    else cout << lo << ' ' << hi << '\n';
    return 0;
}
