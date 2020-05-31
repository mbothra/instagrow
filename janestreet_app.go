package janestreet

import (
	"fmt"
	"os"
	"path"

	"github.com/quickfixgo/fix42/logon"
	"github.com/quickfixgo/fix42/marketdataincrementalrefresh"
	"github.com/quickfixgo/fix42/newordersingle"
	"github.com/quickfixgo/quickfix"
)

type FixApplication struct {
	*quickfix.MessageRouter
}

//Notification of a session begin created.
func (app FixApplication) OnCreate(sessionID quickfix.SessionID) {
	fmt.Println("Created")
	// fmt.Println(sessionID)
	// request := logon.New(field.NewEncryptMethod(enum.EncryptMethod_NONE_OTHER), field.NewHeartBtInt(10))
	// quickfix.SendToTarget(request, sessionID)
	// fmt.Println("Sending Message")
	return
}

//Notification of a session successfully logging on.
func (app FixApplication) OnLogon(sessionID quickfix.SessionID) {
	fmt.Println("On Logon")
	// SendMarketDataRequest(GetSessionIDforSession()
	// SendOrderBookRequest(sessionID)
	return
}

//Notification of a session logging off or disconnecting.
func (app FixApplication) OnLogout(sessionID quickfix.SessionID) {
	fmt.Println("On Logout")
	return
}

func (app FixApplication) ToAdmin(msg *quickfix.Message, sessionID quickfix.SessionID) {
	fmt.Printf("to Admin: %s\n", msg.String())
	// if msg.IsMsgTypeOf("Logon") {
	// 	app.Route(msg, sessionID)
	// }
	return
}

//Notification of app message being sent to target.
func (app FixApplication) ToApp(msg *quickfix.Message, sessionID quickfix.SessionID) (err error) {
	fmt.Printf("To App %s\n", msg.String())
	app.Route(msg, sessionID)
	return
}

//Notification of admin message being received from target.
func (app FixApplication) FromAdmin(msg *quickfix.Message, sessionID quickfix.SessionID) (reject quickfix.MessageRejectError) {
	fmt.Printf("From Admin: %s\n", msg.String())
	return
}

//Notification of app message being received from target.
func (app FixApplication) FromApp(msg *quickfix.Message, sessionID quickfix.SessionID) (reject quickfix.MessageRejectError) {
	fmt.Printf("From App: %s\n", msg.String())
	// app.Route(msg, sessionID)
	return
}

func NewFixApplication() *FixApplication {
	app := &FixApplication{
		MessageRouter: quickfix.NewMessageRouter(),
	}
	app.AddRoute(marketdataincrementalrefresh.Route(app.OnMarketDataRefreshUpdate))
	app.AddRoute(logon.Route(app.OnLogonMessage))
	app.AddRoute(newordersingle.Route(app.OnOrderBookMessage))
	return app
}

func (app *FixApplication) OnMarketDataRefreshUpdate(msg marketdataincrementalrefresh.MarketDataIncrementalRefresh, sessionID quickfix.SessionID) (err quickfix.MessageRejectError) {
	fmt.Printf("%+v\n", msg)
	return
}

func (app *FixApplication) OnLogonMessage(msg logon.Logon, sessionID quickfix.SessionID) (err quickfix.MessageRejectError) {
	msg.SetResetSeqNumFlag(true)
	return
}

func (app *FixApplication) OnOrderBookMessage(msg newordersingle.NewOrderSingle, sessionID quickfix.SessionID) (err quickfix.MessageRejectError) {
	clOrdId, _ := msg.GetClOrdID()
	fmt.Println(clOrdId)
	return nil
}

// func (app *FixApplication) onOrderBookRequest(msg order) {

// }

func main() {
	cfgFileName := path.Join("config", "janestreetfxgo.cfg")

	config, err := os.Open(cfgFileName)
	if err != nil {
		fmt.Printf("Error opening %v, %v\n", cfgFileName, err)
		return
	}
	appSettings, err := quickfix.ParseSettings(config)
	if err != nil {
		fmt.Println("Error reading config file,", err)
		return
	}

	app := NewFixApplication()
	fileLogFactory, err := quickfix.NewFileLogFactory(appSettings)

	if err != nil {
		fmt.Println("Error creating file log factory,", err)
		return
	}

	messageStoreFactory := quickfix.NewMemoryStoreFactory()

	initiator, err := quickfix.NewInitiator(app, messageStoreFactory, appSettings, fileLogFactory)
	if err != nil {
		fmt.Printf("Unable to create Initiator: %s\n", err)
		return
	}

	initiator.Start()
	fmt.Printf("Initiator started")

	// request := logon.New(field.NewEncryptMethod(enum.EncryptMethod_NONE_OTHER), field.NewHeartBtInt(10))
	// quickfix.Send(request)
	// fmt.Printf("Message sent")

	for {
	}

	// initiator.Stop()
}
