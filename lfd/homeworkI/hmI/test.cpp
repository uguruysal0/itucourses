#include <bits/stdc++.h>


using namespace std;

#define pb push_back


vector< vector<char> > v(7);
set<string> res;
char enums[] = {'A','B','C','D','E','F','G'};
void initialize()
{
    v[0].pb('B');
    v[0].pb('G');
    v[0].pb('F'); //A
    v[1].pb('A'),
    v[1].pb('G'),
    v[1].pb('C'); //B
    v[2].pb('D');
    v[2].pb('G');
    v[2].pb('B'); //C
    v[3].pb('E');
    v[3].pb('G');
    v[3].pb('C'); //D
    v[4].pb('D');
    v[4].pb('G');
    v[4].pb('F'); //E
    v[5].pb('A');
    v[5].pb('G');
    v[5].pb('E'); //F
    v[6].pb('A');
    v[6].pb('B');
    v[6].pb('C');
    v[6].pb('D');
    v[6].pb('E');
    v[6].pb('F'); //G
}
bool isContain(const string &s, const char &c)
{
    for(auto &ch: s)  if(ch==c) return true;

    return false;
}

void dfs(int node, string s)
{

    if(s.length()==3) {res.insert(s); return;}
    for(int i=0; i < v[node].size(); ++i) dfs( v[node][i]-65, s + enums[v[node][i]-65]);;
}

int main()
{
    int result = 0;
    initialize();
    for(int i=0; i<7;++i) dfs(i,string(1,enums[i]));
    for(auto &str:res)
    {
        cout << str << endl;
        if(isContain(str,'A')) result++;
    }
    cout << result << "   /     " << res.size() << endl;
    return 0;
} 
