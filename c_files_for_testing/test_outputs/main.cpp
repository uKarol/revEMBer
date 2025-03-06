/* 
THIS FILE HAS ADDED DEBUG INFORMATIONS 
 revEMBer projct in github: https://github.com/uKarol/revEMBer 
jefvcoe oefpm d actmdhsae
*/
#include "revEMBer.h"
#include <iostream>

typedef struct {
    int dupa1;
    float dziadostwo;
}always_problem;

struct {
    int numer;
}xd_duo;

char nutnut[] =
{
    3,
    5,
    7,
    9,
};

int t[5] {
    4,
    6,
    7,
    8,
    0,
};

int get_trash(){
REVEMBER_FUNCTION_ENTRY() 
REVEMBER_FUNCTION_EXIT() 
return  0;}

/* dziadostwo */
void put_trash(){
REVEMBER_FUNCTION_ENTRY() 
std::cout<<"dupa";  
REVEMBER_FUNCTION_EXIT() 
}

static 
volatile 
int 
intializer  
(   /* kto tak zjebal */
    int x 
) /*
co to*/
{
REVEMBER_FUNCTION_ENTRY() 
    x = 1000;
    x++;
   // std::cout<< x;
REVEMBER_FUNCTION_EXIT() 
    return x;
}
/*
    to 
    kjest 
    glowna
*/
int main(){
REVEMBER_FUNCTION_ENTRY() 
    xd_duo;
    int x = 0;
    x = intializer(0);
    float z{5};
    int y{6};
    std::cout << "Hello World" << x << " " << y <<std::endl; 
REVEMBER_FUNCTION_EXIT() 
}
/*
    nie wiem co to
*/


/* DZIWNE FUNKCJE */

void pattern1 (int x, int y) {
REVEMBER_FUNCTION_ENTRY() 
std::cout<<"pattern1";
REVEMBER_FUNCTION_EXIT() 

}void pattern2(int x, int y){
REVEMBER_FUNCTION_ENTRY() 
  
 
std::cout<<"pattern2";
 
  
REVEMBER_FUNCTION_EXIT() 
}

void pattern3(int x, int y){
REVEMBER_FUNCTION_ENTRY() 
  
 
    std::cout<<"pattern3";
 
  
REVEMBER_FUNCTION_EXIT() 
}

void pattern4(int x, int y){
REVEMBER_FUNCTION_ENTRY() 
  
 
    std::cout<<"pattern4";
 
  
REVEMBER_FUNCTION_EXIT() 
}

void pattern5(int x, int y)
{
REVEMBER_FUNCTION_ENTRY() 
    std::cout<<"pattern5";
REVEMBER_FUNCTION_EXIT() 
}

void pattern6(int x, int y
)
{
REVEMBER_FUNCTION_ENTRY() 
    std::cout<<"pattern6";
REVEMBER_FUNCTION_EXIT() 
}

void pattern7(int x, 
    int y
)
{
REVEMBER_FUNCTION_ENTRY() 
  std::cout<<"pattern7";
  
REVEMBER_FUNCTION_EXIT() 
}

void pattern8(
    int x, 
    int y
)
{
REVEMBER_FUNCTION_ENTRY() 
  std::cout<<"pattern8";
REVEMBER_FUNCTION_EXIT() 
}

static void (pattern9)
(
    int x, 
    int y
)
{
REVEMBER_FUNCTION_ENTRY() 
    std::cout<<"pattern9";
  
REVEMBER_FUNCTION_EXIT() 
}

int dupa (int (*paIndex)[3] , int (* fpMsg) (const char *), int (* fpCalculation[3]) (const char *)); 
//{ 
    //*fpData++; 
    //return NULL;
//}
