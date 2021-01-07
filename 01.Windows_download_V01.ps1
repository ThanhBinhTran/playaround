###########################################################################
# HOW TO RUN SCRIPT IN POWERSHELL                                         #
# +---> Open power shell then type ./myscript.ps1"                        #
# THIS SCRIPT USE TO DOWNLOAD FILES FOR WEBSITE                           #
# PARAMETER REQUETSTS FILETYPE AND LINK OF WEBSITE                        #
# AUTHOR: thanhbinh.hcmut@gmail.com                                       #
###########################################################################


#check your arguments
Param (
[Parameter(Mandatory=$True)]
[ValidateNotNull()]
$fileType,
[Parameter(Mandatory=$True)]
[ValidateNotNull()]
$weblink
)

#clean your screen
cls 

#$webpath ="http://1488.unknownsecret.info/mp3/L%E1%BB%87+Quy%C3%AAn/Tr%E1%BA%A3+l%E1%BA%A1i+th%E1%BB%9Di+gian/"
#$webpath ="http://phungminh.96.lt/Nhac%20Xuan%20Vui/"
$DownLoadFileType = $fileType
$webpath  = $weblink

Invoke-WebRequest -outfile list.file $webpath


$maker = "`""
$command_invoke = "Invoke-WebRequest -outfile "

$FileContent = Get-Content list.file


$option = [System.StringSplitOptions]::RemoveEmptyEntries


$separator = "<a href=`"","</a>"
$separator1 = "`">"

$Webseparator = "//", "/"
$subWebPath_temp = $webpath.Split($Webseparator, $option)
$subWebPath = $subWebPath_temp[0] + "://" + $subWebPath_temp[1] + "/"
###$subWebPath

foreach ($element in $FileContent)
{
    #filter line which file type
	if($element.contains($DownLoadFileType))
	{
	    #print for debug
		###Write-Host "======================================="
		###$element    
	
		$hrefLink = $element.Split($separator,$option)
		$herfLink_Name = $hrefLink[1].Split($separator1,$option)
		
		#debug
		###Write-Host "[1--------]"
		###$hrefLink[0]
		###Write-Host "[2--------]"
		###$hrefLink[1]
		###Write-Host "[3--------]"
		###$hrefLink[2]
		
		###Write-Host "[4--------]"
		###$herfLink_Name[0]
		###Write-Host "[5--------]"
		###$herfLink_Name[1]
		
		if($herfLink_Name.contains("/"))
		{
		   $subWebPath = $subWebPath
		}
		else
		{
		   $subWebPath = $webpath
		}
		#index 0 is link
	    $link         = $subWebPath + $herfLink_Name[0].trimStart()
		###$link
		
		#index 1 is name
		$savefile     = $maker + $herfLink_Name[1].trimStart() + $maker + " "
		$command      = $command_invoke + $savefile + $link
		
		#execute command		
		iex $command
		
		#print command
		$command
	}
}