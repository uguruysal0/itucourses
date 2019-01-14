#include <bits/stdc++.h>
/*
 to complie use g++ kod.cpp -O2 -std=c++11
*/
using namespace std;

#define PRINT(x) for(auto &elem: x) {cout << elem << "\n"; }
#define PRINTD(DEBUG) printf("%s\n", DEBUG)
#define ASSERTGRID(g)   for(int i=1; i < g.size(); ++i){  assert( g[i].size() == g[i-1].size()); } 
#define ft first 
#define sd second
#define pb push_back
#define LEN 3

enum DIRECTION { VERTICAL, HORIZONTAL};

typedef int DIRECTON;
typedef pair<int,int> point;
typedef pair<point, DIRECTON> block; 
typedef vector<string> grid;
typedef vector<int> domainList;
typedef vector<block> variableList;
typedef vector<block> blockList;

variableList result; 

struct state{
    variableList listOfBlocks;
    grid gr;
    state(grid a, blockList b){
        gr = a;
        listOfBlocks = b;
    }
    state(){}
};
void makeEmptyGrid(grid &t, int size, int len){
    string toReplace = "";
    for(int i=0; i < len; ++i) toReplace += ".";
    t.clear();
    t.resize(size,toReplace);
}
void myFill( vector<int> &t, int begin, int end  ){
    t.clear();
    t.resize(end-begin);
    for(int i=begin; i < end; ++i){
        t[i-begin] = i;
    }
}
void makeVisitedHorizontal(vector<vector<bool>> &v, int x, int y){
    for(int i=0; i < LEN; ++i){
        v[x][y+i] = true;
    }
}
void makeVisitedVertical(vector<vector<bool>> &v, int x, int y){
    for(int i=0; i < LEN; ++i){
        v[x+i][y] = true;
    }
}
void getBlocks(grid &finalState, blockList &t){
    t.clear();
    /*t = {
        { {5,0}, HORIZONTAL},
        { {0,3}, HORIZONTAL},
        { {1,1}, HORIZONTAL},
        { {1,4}, HORIZONTAL},
        { {2,2}, HORIZONTAL},
        { {2,5}, HORIZONTAL},
        { {2,1}, VERTICAL},
        { {3,3}, VERTICAL},
        { {3,5}, VERTICAL},
    }; */

    vector<vector<bool>> visitedH( finalState.size(), vector<bool>(finalState[0].size(), false));
    vector<vector<bool>> visitedV( finalState.size(), vector<bool>(finalState[0].size(), false));

    /* horizontal pass */
    for(int i=0; i < finalState.size(); ++i ){
        for(int j=0; j  < finalState[0].size(); ++j)
            if ( visitedH[i][j] == false && finalState[i][j] == 'O'){
                t.pb({{i,j}, HORIZONTAL});
                makeVisitedHorizontal(visitedH,i,j);  
            }
    }
    /* vertical pass */
    for(int i=0; i < finalState.size(); ++i ){
        for(int j=0; j  < finalState[0].size(); ++j)
            if ( visitedV[i][j] == false && finalState[i][j] == 'X'){
                t.pb({{i,j}, VERTICAL});
                makeVisitedVertical(visitedV,i,j);
            }
    }
}
void fillVertical(grid &g, point p){
    for(int i=0; i < LEN; ++i){
        g[p.ft+i][p.sd] = 'X';
    }
}
void fillHorizontal(grid &g, point p){
    for(int i=0; i < LEN; ++i){
        g[p.ft][p.sd+i] = 'O';
    }
}
void updateState(state &s){
    grid current = s.gr;
    if ( s.gr.size() > 0){
        makeEmptyGrid(current, s.gr.size(), s.gr[0].size() );
        for ( auto elem: s.listOfBlocks){
            if ( elem.sd == VERTICAL ){
                fillVertical(s.gr, elem.ft);
            }
            else{
                fillHorizontal(s.gr, elem.ft);
            }
        }
    }
    
}
void printState(state &s){
    updateState(s);
    PRINT(s.gr);
}
void printBlocks(blockList &t){
    for(auto block:t){
        if( block.sd == HORIZONTAL){
            cout <<  "HORIZONTAL " <<  block.ft.ft << " " << block.ft.sd  << endl;
        }
        else{
            cout <<  "VERTICAL " <<  block.ft.ft << " " << block.ft.sd  << endl;
        }
    }
}

void dfs(variableList variables, domainList domain, state current, state end, variableList backTrack, bool &isFound){

    if ( domain.size() <= 0 && variables.size() <= 0) {
        isFound = true;
        result=backTrack;
        return;
    }

    for(int i=0; i< variables.size(); ++i){
        auto v = variables[i];
        auto cpyV = variables;
        auto cpyD = domain;
        auto next_val = domain[0];
        auto cpyB = backTrack;
        auto cpyC = current;

        bool satsified = false;

        if ( v.sd == HORIZONTAL){
            auto startPt = v.first;
            startPt.ft++;
            if (  startPt.ft >= current.gr.size()  ){
                satsified = true;
            }
            else if(!satsified){
                if ( cpyC.gr[startPt.ft][startPt.sd+1]!='.' ){
                    satsified= true;
                }
                if( !satsified ){
                    if(cpyC.gr[startPt.ft][startPt.sd]!='.' && cpyC.gr[startPt.ft][startPt.sd+2]!='.'){
                        satsified= true;
                    }
                }
            }
        }
        else{
            auto startPt = v.first;
            startPt.ft+=3;
            if (  startPt.ft >= current.gr.size()  ){
                satsified = true;
            }
            else if(!satsified){
                if ( cpyC.gr[startPt.ft][startPt.sd]!='.' ){
                    satsified= true;
                }
            }
        }
        cpyV.erase(cpyV.begin()+i);
        cpyD.erase(cpyD.begin());
        cpyB.pb(v);

        if ( satsified ) {
            cpyC.listOfBlocks.pb(v);
            updateState(cpyC);
            dfs(cpyV, cpyD, cpyC, end, cpyB,isFound);
        }
        
        
    }
}

void CSPSOLVER(variableList &variables, domainList &domain, state begin, state end){
    printf("This is the target state\n");
    printState(end);
    printf("-----------------\n");
    blockList solution;
    bool isFound= false;
    dfs(variables,domain,begin,end,solution,isFound);
    if( isFound){
        system("sleep 1");
        for( auto elem: result){
            system("clear");
            printf("It is can be built\n");
            begin.listOfBlocks.pb(elem);
            printState(begin);
            system("sleep 1");
          
        }
    }
    else{
        printf("This state is impossible\n");
    }
   
}

int main(){
    
    grid g,empty;
    /* target position */
    g = {
         "...OOO..",
         ".OOOOOO.",
         ".XOOOOOO",
         ".X.X..X.",
         ".X.X..X.",
         "OOOX..X."
        };
    /*
    impossible state
    */
    /*
    g = {
         "..OOO.",
         "..X.X.",
         "..X.X.",
         "..X.X.",
         "OOOOOO",
         "X....X",
         "X....X",
         "X....X"
        };
    */
    makeEmptyGrid(empty, g.size(), g[0].size());
    
    ASSERTGRID(g);
    ASSERTGRID(empty);
    
    blockList targetBlocks, srcBlocks;
    getBlocks(g,targetBlocks);
   
    //printBlocks(targetBlocks);
   
    int numberOfBlock = targetBlocks.size();
    domainList domain;
    myFill(domain, 0, numberOfBlock);

    /* init CSP reqiurements */

    variableList vars = targetBlocks;
    state target(g,targetBlocks), src(empty,srcBlocks);
    CSPSOLVER(vars, domain, src, target);
    
    
    return 0;
}