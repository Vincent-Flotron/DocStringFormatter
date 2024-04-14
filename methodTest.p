  method public void geocodeAddress
    ( input ipcAddress as character,
      output opdLat as decimal,
      output opdLng as decimal,
      output oplStatus as logical,
      output opcMapStatus as character ):
    /* Description -----------------------------------------------------------*/
    /*                                                                        */
    /*                                                                        */
    /*                                                                        */
    /* Notes -----------------------------------------------------------------*/
    /*                                                                        */
    /*                                                                        */
    /*                                                                        */
    /* Parameters ------------------------------------------------------------*/
    /*                                                                        */
    /* <none>                                                                 */
    /*                                                                        */
    /* Examples --------------------------------------------------------------*/
    /*                                                                        */
    /*                                                                        */
    /*                                                                        */
    /*------------------------------------------------------------------------*/
    
    /* Variables -------------------------------------------------------------*/
    /*------------------------------------------------------------------------*/
    
    define variable pcAddrURL         as character format 'x(70)':U           no-undo.
    define variable pcURL             as character format 'x(70)':U           no-undo.
    define variable pcHost            as character format 'x(70)':U           no-undo.
    define variable pcPort            as character format 'x(70)':U           no-undo.
    define variable pcPath            as character format 'x(70)':U           no-undo.
    define variable pcTempFile        as character format 'x(70)':U           no-undo.
    define variable pcResult          as longchar                             no-undo.
                                                                              
    define variable phXML             as handle                               no-undo.
    define variable phRoot            as handle                               no-undo.
                                                                              
    define variable piXMLBegin        as integer   init 0                     no-undo.
    define variable piTempo           as integer   init 1                     no-undo.
    define variable piTimeout         as integer   init 5                     no-undo.
    define variable oResponseJSON     as Progress.Json.ObjectModel.JsonObject no-undo.
    define variable cKey              as character                            no-undo.
    define variable cURI              as character                            no-undo.
    define variable cBaseURL          as character                            no-undo.
    define variable cKeyParam         as character                            no-undo.
    define variable cAddressParam     as character                            no-undo.
    define variable cGoogleMapsApiURL as character                            no-undo.
    
    /* Buffers ---------------------------------------------------------------*/

    /*------------------------------------------------------------------------*/
    /* Processing                                                             */
    /*------------------------------------------------------------------------*/