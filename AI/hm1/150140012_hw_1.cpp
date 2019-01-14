#include <bits/stdc++.h>
using namespace std;   
typedef vector<string> state;
int NUMBEROFPEGS;
struct node{
    state s;
    int depth,cost;
    int heuristiccost;
    int n_children;
    node *parrent;
    static int celem,delem;
    node(state _s ,int _depth, int _cost, node *_parrent) {
        celem++;
        s = _s,depth = _depth,cost=_cost, parrent=_parrent, n_children = 0,heuristiccost=0;
    }
    /*
     deletes nodes from child to parrent, 
     in order to prevent double free, if parrent still has child/children, do not delete it 
    */
    ~node(){
        delem++;
        if ( parrent !=NULL &&  parrent->n_children == 1 ){
            delete parrent;
        } 
        else if ( parrent != NULL){
            parrent->n_children--;
        }
    }
};
/*
    Variables used to see how many nodes deleted and created 
    I checked code with valgrind, I did not see any memory leaks.
 */
int node::celem = 0;
int node::delem = 0;
void print(node &n){
   /*
    print board to see that how the algorithm come up with this state.
   */
    if ( n.parrent == NULL){
        system("clear");
        for( auto elem:n.s){
            cout << elem << endl;
        }
    }
    else{
        print( *(n.parrent) );
        system("clear");
        for( auto elem:n.s){
            cout << elem << endl;
        }
    }
    system("sleep 1");
}
void expand(node &current, list<node *> &expandList){
    /*
        for given "current" node, find all branches and 
        append new nodes to expandList
    */
    auto oldState = current.s;
    function<bool(int,int,int)> isAvailable = [&oldState](int i,int j, int move){
        if ( oldState[i][j] != 'O') 
            return false;
        int new_i= i,new_j = j;
        int inter_i = i, inter_j = j; 
        if (move == 0){
            /* Right (0,1) */
            new_j+=2;
            inter_j++;
        }
        if( move == 1){
            /* Left (0,-1) */
            new_j-=2;
            inter_j--;
        }
        if( move == 2){
            /* Up (-1,0)  */
            new_i-=2;
            inter_i--;
        }
        if (move == 3){
            /* Down (1,0) */
            new_i+=2;
            inter_i++;
        }
        if ( new_i< 0 || new_j < 0 || new_i >= oldState.size() || new_j >=oldState[0].size() ){
            return false;
        }
        if ( inter_i< 0 || inter_j < 0 || inter_i >= oldState.size() || inter_j >=oldState[0].size() ){
            return false;
        }

        if ( oldState[ new_i][ new_j] == '.'){
            if ( oldState[inter_i][inter_j] == 'O' ){
                oldState[new_i][new_j] = 'O';
                oldState[i][j] = '.';
                oldState[inter_i][inter_j] = '.';
                return true;
            }
        }
        return false;
    };
    for(int i=0; i < oldState.size(); ++i){
        for(int j=0; j < oldState[i].size(); ++j){
            for( auto &move:{0,1,2,3}){
                if ( isAvailable(i, j, move)) {
                    current.n_children++;
                    expandList.push_back( new node(oldState, current.depth+1, current.cost+1, &current) ); 
                    oldState = current.s;
                }
            }
        }
    }
}
/*
    All algorithms have nearly same codes, only frontiers are different.
*/
void BFS(state initState){   
    auto start = std::chrono::system_clock::now();
    int maximum_number_in_frontier =0;
    int number_of_nodes_expanded = 0;
    int number_of_nodes_generated = 0;
    auto frontier = queue<node*>();
    auto root =  new node(initState,0,0,NULL); 
    frontier.push(root);
    while( !frontier.empty() ){
        number_of_nodes_expanded++;
        maximum_number_in_frontier = max(maximum_number_in_frontier,(int) frontier.size());
        auto top = frontier.front();
        frontier.pop();
        list<node *> new_nodes = list<node *>();
        expand(*top, new_nodes);
        if(  new_nodes.size() == 0 ){
            
            auto end = std::chrono::system_clock::now();
            print(*top);
            printf("BFS : Cost %d\n", top->cost);
            chrono::duration<double> elapsed_seconds = end-start;
            printf("BFS : Elapsed time: %lf\n", elapsed_seconds.count());

            printf("BFS : Number of nodes generated %d\n", number_of_nodes_generated );
            printf("BFS : Number of nodes expanded %d\n", number_of_nodes_expanded );
            printf("BFS : Maximum number of nodes in frontier %d\n", maximum_number_in_frontier );
            printf("BFS : Number of pegs at final state %d\n",NUMBEROFPEGS-top->cost );

            delete top;
            break;
        }
        number_of_nodes_generated+=(int) new_nodes.size();
        for( auto &elem: new_nodes) { frontier.push(elem); }        
    }
    /* mem clean*/
    while( !frontier.empty() ){
        auto top = frontier.front();
        frontier.pop();
        delete top;      
    }
}
void DFS(state initState){   
    auto start = std::chrono::system_clock::now();
    int maximum_number_in_frontier =0;
    int number_of_nodes_expanded = 0;
    int number_of_nodes_generated = 0;
    auto frontier = stack<node*>(); 
    auto root =  new node(initState,0,0,NULL); 
    frontier.push(root);
    while( !frontier.empty() ){
        number_of_nodes_expanded++;
        maximum_number_in_frontier = max(maximum_number_in_frontier,(int) frontier.size());
        auto top = frontier.top();
        frontier.pop();
        list<node *> new_nodes = list<node *>();
        expand(*top, new_nodes);
        if(  new_nodes.size() == 0 ){
            
            auto end = std::chrono::system_clock::now();
            print(*top);    
            printf("DFS : Cost %d\n", top->cost);
            chrono::duration<double> elapsed_seconds = end-start;
            printf("DFS : Elapsed time: %lf\n", elapsed_seconds.count());

            printf("DFS : Number of nodes generated %d\n", number_of_nodes_generated );
            printf("DFS : Number of nodes expanded %d\n", number_of_nodes_expanded );
            printf("DFS : Maximum number of nodes in frontier %d\n", maximum_number_in_frontier );
            printf("DFS : Number of pegs at final state %d\n",NUMBEROFPEGS-top->cost );
            delete top;
            break;
        }
        number_of_nodes_generated+=(int) new_nodes.size();
        for( auto &elem: new_nodes) { frontier.push(elem); }        
    }
    /* mem clean*/
    while( !frontier.empty() ){
        auto top = frontier.top();
        frontier.pop();
        delete top;      
    }
}
/*take heuristic as parameter, if not given uses constant "0" as heurisic.*/
void AStar(state initState,  function<int(state)> heuristic = [](state){ return 0; } ){       
    auto start = std::chrono::system_clock::now();
    int maximum_number_in_frontier =0;
    int number_of_nodes_expanded = 0;
    int number_of_nodes_generated = 0;
    auto frontier = priority_queue<node*, vector<node*>,
    function<bool(node *a,node *b)> >  ( [](node *a,node *b){ return a->heuristiccost > b->heuristiccost; });
    auto root =  new node(initState,0,0,NULL); 
    frontier.push(root);
    while( !frontier.empty() ){
        number_of_nodes_expanded++;
        maximum_number_in_frontier = max(maximum_number_in_frontier,(int) frontier.size());
        auto top = frontier.top();
        frontier.pop();
        list<node *> new_nodes = list<node *>();
        expand(*top, new_nodes);
        if(  new_nodes.size() == 0 ){
            
            auto end = std::chrono::system_clock::now();
            print(*top);
            printf("A* : Cost, %d Heuristic Value %d\n", top->cost,  top->heuristiccost);

            chrono::duration<double> elapsed_seconds = end-start;
            printf("A* : Elapsed time: %lf\n", elapsed_seconds.count());

            printf("A* : Number of nodes generated %d\n", number_of_nodes_generated );
            printf("A* : Number of nodes expanded %d\n", number_of_nodes_expanded );
            printf("A* : Maximum number of nodes in frontier %d\n", maximum_number_in_frontier );
            printf("A* : Number of pegs at final state %d\n",NUMBEROFPEGS-top->cost );
            delete top;
            break;
        }
        number_of_nodes_generated+=(int) new_nodes.size();
        for( auto &elem: new_nodes) { 
            elem->heuristiccost = elem->cost + heuristic(elem->s);
            frontier.push(elem); 
        }        
    }
    /*mem clean*/
    while( !frontier.empty() ){
        auto top = frontier.top();
        frontier.pop();
        delete top;      
    }
}
/*Helper method*/
bool isAvailable(const state &s ,int i,int j, int move){
        if ( s[i][j] != 'O') 
            return false;
        int new_i= i,new_j = j;
        int inter_i = i, inter_j = j; 
        if (move == 0){
            /* Right (0,1) */
            new_j+=2;
            inter_j++;
        }
        if( move == 1){
            /* Left (0,-1) */
            new_j-=2;
            inter_j--;
        }
        if( move == 2){
            /* Up (-1,0)  */
            new_i-=2;
            inter_i--;
        }
        if (move == 3){
            /* Down (1,0) */
            new_i+=2;
            inter_i++;
        }
        if ( new_i< 0 || new_j < 0 || new_i >= s.size() || new_j >=s[0].size() ){
            return false;
        }
        if ( inter_i< 0 || inter_j < 0 || inter_i >= s.size() || inter_j >=s[0].size() ){
            return false;
        }

        if ( s[ new_i][ new_j] == '.'){
            if ( s[inter_i][inter_j] == 'O' ){
                return true;
            }
        }
        return false;
};
int heuristic_1 (const state &s) {
    /*
        I tried to generate all possible situtation of board and calculated costs from these states.
        for example
        ..OO. 
        .OO.
        Above state, all pegs can move, its cost is one. So I count number of pegs can move and divide it 4
        Then ceil.
    */
    int res = 0;
    for (int i=0; i < s.size(); ++i){
        for (int j =0 ; j < s[0].size(); ++j){
            for (int m: {0,1,2,3}){
                if ( isAvailable(s,i,j,m)){
                    res++;
                }
            }
        }
    }
    return (int)ceil( (double)res/4.0);
}
int heuristic_2 (const state &s) {
    /*
        This heuristic is not admissible for all states. But from initial state(standard solo test)
        it is addmissible. Cost can not be greater than 6. 
    */
    int res = 0;
    for (int i=0; i < s.size(); ++i){
        for (int j =0 ; j < s[0].size(); ++j){
            for (int m: {0,1,2,3}){
                if ( isAvailable(s,i,j,m)){
                    res++;
                }
            }
        }
    }
    return min(res,6);
}
void usage(){
    puts("Usage");
    puts("For DFS give \"DFS\" as arguman ");
    puts("For BFS give \"BFS\" as arguman ");
    puts("For Astar  give \"Astar (<h1> or <h2>)\" as arguman ");
}
int main(int argc , char **argv ){ 
    /*Test program for algorithms */
    if ( argc == 1){
        usage();
        return 0;
    }
    state initialState = {
    "  OOO  ",
    "  OOO  ",
    "OOOOOOO",
    "OOO.OOO",
    "OOOOOOO",
    "  OOO  ",
    "  OOO  "
    };

    /* different initial positions to check that is heuristic admissible, can A* find optimal solution?*/

    // initialState = {
    //     "     ..",
    //     "   ..OO",
    //     "  .OO. ",
    //     " .OO.  ",
    //     ".OO.   ",
    //     "  .    ",
    //     "       "
    // };

    for(auto &elem: initialState){for(auto &c: elem) { if (c=='O') NUMBEROFPEGS++ ; } }
    if ( strcmp(argv[1], "DFS") == 0 ){
        DFS(initialState);    
    }
    else if ( strcmp( argv[1], "BFS" ) == 0 ){
        BFS(initialState);
    }
    else if ( strcmp(argv[1], "Astar") ==0 ) {
        if ( argc != 3){
            usage();
            return 0;
        }
        if ( strcmp(argv[2], "h1") == 0 ){
            AStar(initialState,heuristic_1);
        }
        else if( strcmp(argv[2], "h2") == 0 ){
            AStar(initialState,heuristic_2);
        }
    }
    else{
        usage();
    }

    return 0;
}