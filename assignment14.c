#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_QUAD 100

// Quadruple structure
typedef struct {
    char op[10];
    char arg1[10];
    char arg2[10];
    int target;
} Quadruple;

Quadruple quad[MAX_QUAD];
int quad_index = 0;

// Linked list node for backpatching instruction indices
typedef struct Node {
    int index;
    struct Node* next;
} Node;

typedef struct {
    Node* head;
} List;

// Struct to hold true and false lists for boolean expressions
typedef struct {
    List* truelist;
    List* falselist;
} BoolExpr;

// Input string buffer and position pointer
char input[256];
int pos = 0;

// Function declarations
int emit(const char* op, const char* arg1, const char* arg2, int target);
List* makelist(int i);
List* mergelist(List* l1, List* l2);
void backpatch(List* l, int target);

BoolExpr parse_expr();
BoolExpr parse_term();
BoolExpr parse_factor();
BoolExpr parse_condition();

// Skip whitespace in user input
void skip_whitespace() {
    while (input[pos] == ' ' || input[pos] == '\t' || input[pos] == '\r' || input[pos] == '\n') {
        pos++;
    }
}

// Emit a new quadruple instruction
int emit(const char* op, const char* arg1, const char* arg2, int target) {
    strcpy(quad[quad_index].op, op);
    strcpy(quad[quad_index].arg1, arg1);
    strcpy(quad[quad_index].arg2, arg2);
    quad[quad_index].target = target;
    return quad_index++;
}

// Create a list with a single instruction index
List* makelist(int i) {
    List* l = (List*)malloc(sizeof(List));
    l->head = (Node*)malloc(sizeof(Node));
    l->head->index = i;
    l->head->next = NULL;
    return l;
}

// Merge two lists
List* mergelist(List* l1, List* l2) {
    if (!l1) return l2;
    if (!l2) return l1;
    Node* temp = l1->head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = l2->head;
    return l1;
}

// Backpatch instructions in the list with target label
void backpatch(List* l, int target) {
    Node* temp = l ? l->head : NULL;
    while (temp != NULL) {
        quad[temp->index].target = target;
        temp = temp->next;
    }
}

// --- Recursive Descent Parser with Backpatching ---

// E -> E || M Term
BoolExpr parse_expr() {
    BoolExpr node1 = parse_term();
    skip_whitespace();
    
    while (input[pos] == '|' && input[pos+1] == '|') {
        pos += 2; // skip "||"
        int m_quad = quad_index; // Marker for backpatching target
        
        backpatch(node1.falselist, m_quad); // If node1 is false, jump to term
        
        BoolExpr node2 = parse_term();
        
        BoolExpr result;
        result.truelist = mergelist(node1.truelist, node2.truelist);
        result.falselist = node2.falselist;
        node1 = result;
        skip_whitespace();
    }
    return node1;
}

// Term -> Term && M Factor
BoolExpr parse_term() {
    BoolExpr node1 = parse_factor();
    skip_whitespace();
    
    while (input[pos] == '&' && input[pos+1] == '&') {
        pos += 2; // skip "&&"
        int m_quad = quad_index; // Marker for backpatching target
        
        backpatch(node1.truelist, m_quad); // If node1 is true, jump to factor
        
        BoolExpr node2 = parse_factor();
        
        BoolExpr result;
        result.truelist = node2.truelist;
        result.falselist = mergelist(node1.falselist, node2.falselist);
        node1 = result;
        skip_whitespace();
    }
    return node1;
}

// Factor -> ! Factor | ( E ) | ID RELOP ID
BoolExpr parse_factor() {
    skip_whitespace();
    BoolExpr result;

    if (input[pos] == '!') {
        pos++;
        result = parse_factor();
        // Swap truelist and falselist for NOT operator
        List* temp = result.truelist;
        result.truelist = result.falselist;
        result.falselist = temp;
        return result;
    }
    else if (input[pos] == '(') {
        pos++; // skip '('
        result = parse_expr();
        skip_whitespace();
        if (input[pos] == ')') pos++; // skip ')'
        return result;
    }
    else {
        return parse_condition();
    }
}

// Condition -> ID RELOP ID (e.g., a<b, x==y)
BoolExpr parse_condition() {
    skip_whitespace();
    char id1[20], relop[5], id2[20];
    int i = 0;

    // Read first identifier/number
    while (isalnum(input[pos])) {
        id1[i++] = input[pos++];
    }
    id1[i] = '\0';

    skip_whitespace();

    // Read relational operator (<, >, <=, >=, ==, !=)
    i = 0;
    while (input[pos] == '<' || input[pos] == '>' || input[pos] == '=' || input[pos] == '!') {
        relop[i++] = input[pos++];
    }
    relop[i] = '\0';

    skip_whitespace();

    // Read second identifier/number
    i = 0;
    while (isalnum(input[pos])) {
        id2[i++] = input[pos++];
    }
    id2[i] = '\0';

    // Build jump instructions
    char jump_op[10];
    sprintf(jump_op, "j%s", relop); // e.g., "j<"

    int true_jump = emit(jump_op, id1, id2, -1);
    int false_jump = emit("goto", "", "", -1);

    BoolExpr res;
    res.truelist = makelist(true_jump);
    res.falselist = makelist(false_jump);
    return res;
}

// Print generated quadruples
void print_code() {
    printf("\n==================================================\n");
    printf("     GENERATED INTERMEDIATE CODE (QUADRUPLES)     \n");
    printf("==================================================\n");
    for (int i = 0; i < quad_index; i++) {
        if (quad[i].target == -1)
            printf("%d: (%s, %s, %s,  -> unpatched)\n", i, quad[i].op, quad[i].arg1, quad[i].arg2);
        else
            printf("%d: (%s, %s, %s,  -> %d)\n", i, quad[i].op, quad[i].arg1, quad[i].arg2, quad[i].target);
    }
    printf("==================================================\n\n");
}

int main() {
    printf("Enter a boolean expression (e.g., a<b || c<d && e>f): \n> ");
    if (fgets(input, sizeof(input), stdin) != NULL) {
        // Remove trailing newline if present
        input[strcspn(input, "\r\n")] = 0;

        quad_index = 0;
        pos = 0;

        BoolExpr final_expr = parse_expr();

        // Backpatch final expression exits to success/failure labels (e.g., placeholder index quad_index)
        backpatch(final_expr.truelist, quad_index);
        emit("label", "TRUE_EXIT", "", -1);

        backpatch(final_expr.falselist, quad_index);
        emit("label", "FALSE_EXIT", "", -1);

        print_code();
    }
    return 0;
}