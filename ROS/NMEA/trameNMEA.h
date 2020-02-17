#ifndef TRAMENMEA_H
#define TRAMENMEA_H
#include <string>
class TrameNMEA{
    private:
        std::string *strIdTrame=new std::string[87]{
            "AAM", // Waypoint Arrival Alarm
            "ALM", // - GPS Almanac Data
            "APA", // - Autopilot Sentence "A"
            "APB",// - Autopilot Sentence "B"
            "BOD",// - Bearing - Waypoint to Waypoint
            "BWC",// - Bearing & Distance to Waypoint - Great Circle
            "BWR",// - Bearing and Distance to Waypoint - Rhumb Line
            "BWW",// - Bearing - Waypoint to Waypoint
            "DBK",// - Depth Below Keel
            "DBS",// - Depth Below Surface
            "DBT",// - Depth below transducer
            "DCN",// - Decca Position
            "DPT",// - Depth of Water
            "DTM",// - Datum Reference
            "FSI",// - Frequency Set Information
            "GBS",// - GPS Satellite Fault Detection
            "GGA",// - Global Positioning System Fix Data
            "GLC",// - Geographic Position, Loran-C
            "GLL",// - Geographic Position - Latitude/Longitude
            "GNS",// - Fix data
            "GRS",// - GPS Range Residuals
            "GST",// - GPS Pseudorange Noise Statistics
            "GSA",// - GPS DOP and active satellites
            "GSV",// - Satellites in view
            "GTD",// - Geographic Location in Time Differences
            "GXA",// - TRANSIT Position - Latitude/Longitude
            "HDG",// - Heading - Deviation & Variation
            "HDM",// - Heading - Magnetic
            "HDT",// - Heading - True
            "HFB",// - Trawl Headrope to Footrope and Bottom
            "HSC",// - Heading Steering Command
            "ITS",// - Trawl Door Spread 2 Distance
            "LCD",// - Loran-C Signal Data
            "MDA",// - Meteorilogical Composite
            "MSK",// - Control for a Beacon Receiver
            "MSS",// - Beacon Receiver Status
            "MTW",// - Mean Temperature of Water
            "MWV",// - Wind Speed and Angle
            "OLN",// - Omega Lane Numbers
            "OSD",// - Own Ship Data
            "R00",// - Waypoints in active route
            "RMA",// - Recommended Minimum Navigation Information
            "RMB",// - Recommended Minimum Navigation Information
            "RMC",// - Recommended Minimum Navigation Information
            "ROT",// - Rate Of Turn
            "RPM",// - Revolutions
            "RSA",// - Rudder Sensor Angle
            "RSD",// - RADAR System Data
            "RTE",// - Routes
            "SFI",// - Scanning Frequency Information
            "STN",// - Multiple Data ID
            "TDS",// - Trawl Door Spread Distance
            "TFI",// - Trawl Filling Indicator
            "TLB",// - Target Label
            "TLL",// - Target Latitude and Longitude
            "TPC",// - Trawl Position Cartesian Coordinates
            "TPR",// - Trawl Position Relative Vessel
            "TPT",// - Trawl Position True
            "TRF",// - TRANSIT Fix Data
            "TTM",// - Tracked Target Message
            "VBW",// - Dual Ground/Water Speed
            "VDR",// - Set and Drift
            "VHW",// - Water speed and heading
            "VLW",// - Distance Traveled through Water
            "VPW",// - Speed - Measured Parallel to Wind
            "VTG",// - Track made good and Ground speed
            "VWR",// - Relative Wind Speed and Angle
            "WCV",// - Waypoint Closure Velocity
            "WNC",// - Distance - Waypoint to Waypoint
            "WPL",// - Waypoint Location
            "XDR",// - Transducer Measurement
            "XTE",// - Cross-Track Error, Measured
            "XTR",// - Cross Track Error - Dead Reckoning
            "ZDA",// - Time & Date - UTC, day, month, year and local time zone
            "ZFO",// - UTC & Time from origin Waypoint
            "ZTG",// - UTC & Time to Destination Waypoint
            "PASHR",// - RT300 proprietary roll and pitch sentence
            "PGRME",// - Garmin Estimated Error
            "PGRMZ",// - Garmin Altitude
            "PMGNS",// - Magellan Status
            "PRWIZCH",// - Rockwell Channel Status
            "PUBX_00",// - u-blox Lat/Long Position Data
            "PUBX_01",// - u-blox UTM Position Data
            "PUBX_03",// - u-blox Satellite Status
            "PUBX_04",// - u-blox Time of Day and Clock Information
            "TMVTD",// - Transas VTS / SML tracking system report
            "None"};
    

    public:
        typedef enum{GP=0,LC=1,OM=2,II=3, None=100} iDrecepteur;
        //typedef enum{GGA=0, GLL=1, GSA=2, GSV=3, VTG=4, RMC=5} iDtrame;
        typedef enum{ //source https://gpsd.gitlab.io/gpsd/NMEA.html
            AAM=0, // Waypoint Arrival Alarm
            ALM=1, // - GPS Almanac Data
            APA=2, // - Autopilot Sentence "A"
            APB=3,// - Autopilot Sentence "B"
            BOD=4,// - Bearing - Waypoint to Waypoint
            BWC=5,// - Bearing & Distance to Waypoint - Great Circle
            BWR=6,// - Bearing and Distance to Waypoint - Rhumb Line
            BWW=7,// - Bearing - Waypoint to Waypoint
            DBK=8,// - Depth Below Keel
            DBS=9,// - Depth Below Surface
            DBT=10,// - Depth below transducer
            DCN=11,// - Decca Position
            DPT=12,// - Depth of Water
            DTM=13,// - Datum Reference
            FSI=14,// - Frequency Set Information
            GBS=15,// - GPS Satellite Fault Detection
            GGA=16,// - Global Positioning System Fix Data
            GLC=17,// - Geographic Position, Loran-C
            GLL=18,// - Geographic Position - Latitude/Longitude
            GNS=19,// - Fix data
            GRS=20,// - GPS Range Residuals
            GST=21,// - GPS Pseudorange Noise Statistics
            GSA=22,// - GPS DOP and active satellites
            GSV=23,// - Satellites in view
            GTD=24,// - Geographic Location in Time Differences
            GXA=25,// - TRANSIT Position - Latitude/Longitude
            HDG=26,// - Heading - Deviation & Variation
            HDM=27,// - Heading - Magnetic
            HDT=28,// - Heading - True
            HFB=29,// - Trawl Headrope to Footrope and Bottom
            HSC=30,// - Heading Steering Command
            ITS=31,// - Trawl Door Spread 2 Distance
            LCD=32,// - Loran-C Signal Data
            MDA=33,// - Meteorilogical Composite
            MSK=34,// - Control for a Beacon Receiver
            MSS=35,// - Beacon Receiver Status
            MTW=36,// - Mean Temperature of Water
            MWV=37,// - Wind Speed and Angle
            OLN=38,// - Omega Lane Numbers
            OSD=39,// - Own Ship Data
            R00=40,// - Waypoints in active route
            RMA=41,// - Recommended Minimum Navigation Information
            RMB=42,// - Recommended Minimum Navigation Information
            RMC=43,// - Recommended Minimum Navigation Information
            ROT=44,// - Rate Of Turn
            RPM=45,// - Revolutions
            RSA=46,// - Rudder Sensor Angle
            RSD=47,// - RADAR System Data
            RTE=48,// - Routes
            SFI=49,// - Scanning Frequency Information
            STN=50,// - Multiple Data ID
            TDS=51,// - Trawl Door Spread Distance
            TFI=52,// - Trawl Filling Indicator
            TLB=53,// - Target Label
            TLL=54,// - Target Latitude and Longitude
            TPC=55,// - Trawl Position Cartesian Coordinates
            TPR=56,// - Trawl Position Relative Vessel
            TPT=57,// - Trawl Position True
            TRF=58,// - TRANSIT Fix Data
            TTM=59,// - Tracked Target Message
            VBW=60,// - Dual Ground/Water Speed
            VDR=61,// - Set and Drift
            VHW=62,// - Water speed and heading
            VLW=63,// - Distance Traveled through Water
            VPW=64,// - Speed - Measured Parallel to Wind
            VTG=65,// - Track made good and Ground speed
            VWR=66,// - Relative Wind Speed and Angle
            WCV=67,// - Waypoint Closure Velocity
            WNC=68,// - Distance - Waypoint to Waypoint
            WPL=69,// - Waypoint Location
            XDR=70,// - Transducer Measurement
            XTE=71,// - Cross-Track Error, Measured
            XTR=72,// - Cross Track Error - Dead Reckoning
            ZDA=73,// - Time & Date - UTC, day, month, year and local time zone
            ZFO=74,// - UTC & Time from origin Waypoint
            ZTG=75,// - UTC & Time to Destination Waypoint
            //Other sentences
            //Vendor extensions

            PASHR=76,// - RT300 proprietary roll and pitch sentence
            PGRME=77,// - Garmin Estimated Error
            PGRMZ=78,// - Garmin Altitude
            PMGNST=79,// - Magellan Status
            PRWIZCH=80,// - Rockwell Channel Status
            PUBX_00=81,// - u-blox Lat/Long Position Data
            PUBX_01=82,// - u-blox UTM Position Data
            PUBX_03=83,// - u-blox Satellite Status
            PUBX_04=84,// - u-blox Time of Day and Clock Information
            TMVTD=85,// - Transas VTS / SML tracking system report
            } iDtrame;

        
        TrameNMEA::iDtrame convertStr2IdTrame(std::string idT);
        TrameNMEA::iDrecepteur recepteur;
        TrameNMEA::iDtrame trame;
        std::string *message;

        TrameNMEA::TrameNMEA(TrameNMEA::iDrecepteur idrecepteur, TrameNMEA::iDtrame idtrame, std::string *message);
        //TrameNMEA::TrameNMEA(void);


};
#endif