
   sqlquery='select stocklist.wind_code ,stocklist.sec_name from quantaxis.stocklist';
                    curs = fetch(exec(app.INT_MYSQL.Conn,sqlquery));
                    
                    app.ACC.StockList=curs.Data;
                    app.ACC_ID=1;
                    app.ACC.Type='ts';
                    app.ACC.StockId=char(app.ACC.StockList(1,1));
                    notify(app,'SQL')
                    app.ACC.StockId=char(app.ACC.StockList(2,1));
                    notify(app,'SQL')
                    app.ACC_Methods.AnalysisID=1;
                    app.ACC_Methods.AnalysisName=app.ACC.UseData{app.ACC_Methods.AnalysisID,1};
                    app.ACC_Methods.AnalysisData=app.ACC.UseData{app.ACC_Methods.AnalysisID,2};
                    app.ACC_Methods.AnalysisObj=cell2mat(app.ACC_Methods.AnalysisData(:,2));
                    app.ACC_Methods.Date=app.ACC_Methods.AnalysisData(:,1);
                    
                    
                    ShortLen = 5;
                    LongLen = 20;
                    testx=app.ACC_Methods.AnalysisObj;
                    [MA5, MA20] = movavg(testx', ShortLen, LongLen);
                    MA5(1:ShortLen-1) = app.ACC_Methods.AnalysisObj(1:ShortLen-1);
                    MA20(1:LongLen-1) = app.ACC_Methods.AnalysisObj(1:LongLen-1);
                    
                    
                    for t = LongLen:length(app.ACC_Methods.AnalysisObj)
                        
                        %
                        SignalBuy = MA5(t)>MA5(t-1) && MA5(t)>MA20(t) && MA5(t-1)>MA20(t-1) && MA5(t-2)<=MA20(t-2);
                        %
                        SignalSell = MA5(t)<MA5(t-1) && MA5(t)<MA20(t) && MA5(t-1)<MA20(t-1) && MA5(t-2)>=MA20(t-2);
                        
                        %
                        if SignalBuy == 1  && app.ACC_Cash>0
                            
                            
                            app.MES.Str=['Decision -- Buy',app.ACC_Methods.AnalysisName];
                            disp(app.MES.Str)
                            notify(app,'MESSAGE')
                            app.TRA.id=app.ACC_Methods.AnalysisName;
                            app.TRA.Date=app.ACC_Methods.Date(t);
                            app.TRA.Date=app.TRA.Date{1,1};
                            app.TRA.Bid=app.ACC_Methods.AnalysisObj(t);
                            app.TRA.Amount=10000;
                            app.TRA.Position=-1;
                            notify(app,'TRADE')
                            
                        end
                        
                        %
                        if SignalSell == 1 && app.ACC_Account{2,2}>0
                            %
                            
                            app.MES.Str=['Decision -- SELL',app.ACC_Methods.AnalysisName];
                            disp(app.MES.Str)
                            notify(app,'MESSAGE')
                            app.TRA.id=app.ACC_Methods.AnalysisName;
                            app.TRA.Date=app.ACC_Methods.Date(t);
                            app.TRA.Date=app.TRA.Date{1,1};
                            app.TRA.Bid=app.ACC_Methods.AnalysisObj(t);
                            app.TRA.Amount=10000;
                            app.TRA.Position=1;
                            notify(app,'TRADE')
                        end
                        
                        
                        %
                        if t == length(app.ACC_Methods.AnalysisObj) && app.ACC_Account{2,2}>0
                            app.MES.Str=['Decision -- SELL',app.ACC_Methods.AnalysisName];
                            disp(app.MES.Str)
                            notify(app,'MESSAGE')
                            app.TRA.id=app.ACC_Methods.AnalysisName;
                            app.TRA.Date=app.ACC_Methods.Date(t);
                            app.TRA.Date=app.TRA.Date{1,1};
                            app.TRA.Bid=app.ACC_Methods.AnalysisObj(t);
                            app.TRA.Amount=app.ACC_Account{2,2};
                            app.TRA.Position=1;
                            notify(app,'TRADE')
                        end
                        
                    end