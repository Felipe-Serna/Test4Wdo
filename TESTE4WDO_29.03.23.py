//+------------------------------------------------------------------+
//|                                                       teste4.mq5 |
//|                                                     Felipe Serna |
//|                                      https://www.feliseperna.com |
//+------------------------------------------------------------------+
#property copyright "Felipe Serna"
#property link      "https://www.feliseperna.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
#include  <Trade\Trade.mqh>

CTrade trade ;

input ulong    LOTES  = 1 ; // LOTES
input double   TP = 4.5 ;   // TAKE PROFIT
input double   SL = 4.5 ;   // STOP LOSS

MqlTick tick ;
MqlTick ticks [] ;
MqlRates rate [] ;
MqlBookInfo book [] ;

int OnInit()
  {

  MarketBookAdd( _Symbol ) ; 
  #define LENGHT 64  
  
  return(INIT_SUCCEEDED);

  }
  
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
  
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+

void OnTick() {
//======================================================================================

ArraySetAsSeries ( ticks , true ) ;
ArraySetAsSeries ( rate , true ) ;
SymbolInfoTick   ( _Symbol,tick );

int copied = CopyTicks ( _Symbol , ticks , COPY_TICKS_TRADE , 0 , 121 ) ;  
int copiedd = CopyRates( _Symbol , _Period , 0 , 5 , rate) ;
if (copiedd < 3) return ;


//TEMPO ENTRE TICKS ===================================================================

long tempo =  (ticks[0].time - ticks[60].time) ; 
long tempo2 = (ticks[61].time - ticks[120].time) ; 

// SALDO BOOK ==========================================================================

MarketBookGet ( _Symbol , book ) ;
string output ;
for ( int index = 0 ; index < ArraySize(book) ; index++  )

  {
    long saldo = ( ( book[ 32 ].volume + book[ 33 ].volume + book[ 34 ].volume + book[ 35 ].volume + book[ 36 ].volume ) - 
                   ( book[ 31 ].volume + book[ 30 ].volume + book[ 29 ].volume + book[ 28 ].volume + book[ 27 ].volume )  ) ;

   output = output+ 

   " SALDO : " + IntegerToString ( saldo ) +
   " TEMPO : " + (string) tempo +
   "\n" ;
 
  }  
  
Comment ( output ) ;  

//MÉDIA MÓVEL ==========================================================================

  double ask , bid , last ; 
  
  
  ask = SymbolInfoDouble (_Symbol , SYMBOL_ASK ) ; 
  bid = SymbolInfoDouble (_Symbol , SYMBOL_BID ) ;  
  last = SymbolInfoDouble (_Symbol , SYMBOL_LAST ) ; 
  
  
  double smalonga[] ; 
  int    smaHandle2 ;
  
  smaHandle2 = iMA ( _Symbol , _Period , 20 , 0 , MODE_SMA , PRICE_CLOSE ) ;         
  ArraySetAsSeries (smalonga , true ) ; 
  CopyBuffer (smaHandle2 , 0 , 0 , 20 , smalonga ) ;

//VOLUMES =============================================================================

double VolumeArray[];
int VolumeHandle ; 
VolumeHandle = iVolumes (_Symbol, PERIOD_M1, VOLUME_REAL);
ArraySetAsSeries(VolumeArray , true);
CopyBuffer (VolumeHandle , 0 , 0 , 11 , VolumeArray ) ;

// SALDO VARIÁVEL GLOBAL ===============================================================

long saldo = ( ( book[ 32 ].volume + book[ 33 ].volume + book[ 34 ].volume + book[ 35 ].volume + book[ 36 ].volume ) - 
               ( book[ 31 ].volume + book[ 30 ].volume + book[ 29 ].volume + book[ 28 ].volume + book[ 27 ].volume )  ) ;


// RETURNS ============================================================================

if ( OrdersTotal() >= 1 ) return ;
if ( ! SymbolInfoTick ( _Symbol , tick ) ) return ;
if ( PositionsTotal() > 0) return ;

   if ((ticks[61].time - ticks[120].time) > 8) return ;
   if ((ticks[0].time - ticks[60].time) > 5) return ;

   if ( PositionsTotal() >= 1 ) Sleep (120000) ;


// ORDENS COMPRA E VENDA ===============================================================


//ORDEM COMPRA --------------------------

  if
   
      ( 
         
         (ticks[0].time-ticks[60].time) < (ticks[61].time-ticks[120].time)
     
       && last > rate[1].close
      
       && (last - ask) >= 1.5
   
       && last > smalonga[0]
   
       && saldo < -1
  
       && smalonga[0]>smalonga[1] && smalonga[1]>smalonga[2] && smalonga[2]>smalonga[3] && smalonga[3]>smalonga[4] && smalonga[4]>smalonga[5] 
   
       && last - smalonga[0] <= 8

      )
     
     {
   
     BuyMarket ( LOTES , tick.last - SL , tick.last + TP ) ;

     Print ( VolumeArray[0] + VolumeArray[1] + VolumeArray[2] + VolumeArray[3] + VolumeArray[4] + VolumeArray[5]
           + VolumeArray[6] + VolumeArray[7] + VolumeArray[8] + VolumeArray[9] + VolumeArray[10]) ;

     Print (  
         " COMPRA " , 
         " PULO " , ( last - ask ) ,
         " Tempo " , tempo , 
         " tempo antes " , tempo2 , 
         " last " , last , 
         " bid pedra compra " , bid , 
         " ask pedra venda " , ask , 
         " (tick 0-tick 10): " , (ticks[0].last - ticks[10].last) ,
         " (tick 0-tick 60): " , (ticks[0].last - ticks[60].last) , 
         " SALDO " , output
         
           );

     }
 
   
// ORDEM VENDA ---------------------------------------------
   
  if 
  
   ( 
   
  (ticks[0].time - ticks[60].time) < (ticks[61].time - ticks[120].time)
   
  && last < rate[1].close
      
  && (bid - last) >= 1.5
   
  && last < smalonga[0] 
      
  && saldo > 1
    
  && smalonga[0]<smalonga[1] && smalonga[1]<smalonga[2] && smalonga[2]<smalonga[3] && smalonga[3]<smalonga[4] && smalonga[4]<smalonga[5] 
                                                               
  && smalonga[0] - last <= 8 
      
   )

   {
   
   SellMarket ( LOTES , tick.last + SL , tick.last - TP ) ;
   
  
   Print (VolumeArray[0] + VolumeArray[1] + VolumeArray[2]+ VolumeArray[3] + VolumeArray[4]+VolumeArray[5]
         +VolumeArray[6]+VolumeArray[7]+VolumeArray[8]+VolumeArray[9]+VolumeArray[10]) ;

   Print ( 
         " VENDA " , 
         " PULO " , ( bid - last ) ,
         " Tempo " , tempo ,
         " tempo antes " , tempo2 , 
         " last ", last ,
         " bid pedra compra " , bid , 
         " ask pedra venda " , ask , 
         " (tick 10-tick 0): " , (ticks[10].last - ticks[0].last) ,
         " (tick 60-tick 0): " , (ticks[60].last - ticks[0].last) ,
         " SALDO " , output
         
         );
             
   }
    
// END ORDENS COMPRA E VENDA ==================================================================================
  
}

//+-------------------------------------------------------------------+
// END ONTICK
//+-------------------------------------------------------------------+


bool BuyMarket (ulong _volume , double _sl , double _tp) {
bool ok = trade.Buy ( _volume , _Symbol , 0.0 , _sl , _tp );
if ( ! ok ) {
int errorCode = GetLastError();
Print ("BuyMarket: " , errorCode ) ;
ResetLastError();

}

return ok ;

}


bool SellMarket ( ulong _volume , double _sl , double _tp) {
bool ok = trade.Sell ( _volume , _Symbol , 0.0 , _sl , _tp ) ;
if ( ! ok ) {
int errorCode = GetLastError();
Print ("SellMarket: " , errorCode ) ;
ResetLastError();

}

return ok ;

}