const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const ev3dev = require('ev3dev-lang');


function printBatteryInfo(label, battery) {
	console.log(label + " --------------");
	
	if(battery.connected) {	
		console.log('  Technology: ' + battery.technology);
		console.log('  Type: ' + battery.type);
		
		console.log('  Current (microamps): ' + battery.measuredCurrent);
		console.log('  Current (amps): ' + battery.currentAmps);
		
		console.log('  Voltage (microvolts): ' + battery.measuredVoltage);
		console.log('  Voltage (volts): ' + battery.voltageVolts);
		
		console.log('  Max voltage (microvolts): ' + battery.maxVoltage);
        console.log('  Min voltage (microvolts): ' + battery.minVoltage);
        
        Console.log('  Battery % is (probably almost sort of but not really): ' + battery.measuredVoltage/battery.maxVoltage)
	}
	else
	    console.log("  Battery not connected!");
}

var defaultBattery = new ev3dev.PowerSupply();
printBatteryInfo("Default battery", defaultBattery);

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});