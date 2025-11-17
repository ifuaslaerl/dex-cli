#include <bits/stdc++.h>
using namespace std;

// g++ -Dlocal file.cpp

#ifdef local
    #include ".debug.h"
    #define pr(...) debug(#__VA_ARGS__, __VA_ARGS__)
    #define prs(...) debug_nameless(__VA_ARGS__)
#else
    #define pr(...) 69
    #define prs(...) 69
#endif

#define fastio ios_base::sync_with_stdio(NULL); cin.tie(nullptr)

typedef long double ld;
typedef long long ll;

const int inf = 2e9;
const ll INF = 2e18;

// Copy-Pasted Code


// Global Variables


void solve(int test_case){
}

int main(){
    fastio;

    int t=1;
    cin >> t;
    for(int testCase=1; testCase<=t; testCase++){
	#ifdef local
		cout << "---------------------------------------------\n";
	#endif
	pr(testCase);
	solve(testCase);
	#ifdef local
   		cout << "---------------------------------------------\n";
		cout << "\n";
	#endif
    }

    return 0;
}
