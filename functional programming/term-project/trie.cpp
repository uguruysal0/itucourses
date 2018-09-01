#include <bits/stdc++.h>

using namespace std;

#define fs first
#define sd second
#define max3(a,b,c) max(a,max(b,c))
#define min3(a,b,c) min(a,min(b,c))
#define pb push_back

typedef long long int ll;
typedef pair<int,int> ii;
typedef vector<int> vi;
typedef vector<vi> vii;


class Trie{
private:
    struct node{
        map<char,node> children;
        bool isEnd;
        node(){isEnd = false;}
    };
    node root;
public:
    Trie(){}
    void insert(const string &s){
        auto trv = &root;
        for(int i=0; i < s.length();++i){
            if( trv->children.find(s[i])!=trv->children.end() ){
                trv = &(trv->children[s[i]]);
            }
            else{
                trv->children[s[i]] = node();
                trv = &(trv->children[s[i]]);
            }
        }
        trv->isEnd = true;
    }
    void insertList(const string []){}
    bool search(const string &s){
        bool res = false;
        auto trv = &root;
        for (auto c:s){
            if( trv->children.find( c )!=trv->children.end() ){
                trv = &(trv->children[c]);
                res = trv->isEnd;
            }
            else{
                return false;
            }
        }
        return res;

    }
    vector<string> getWords(){}
    vector<string> prefix(string &s){}
};
int main(){
    std::ios::sync_with_stdio(false);
    Trie a;
    a.insert("abc");
    a.insert("abce");
    if (a.search("abcd")){
        cout <<"asd" << endl;
    }

    return 0;
}