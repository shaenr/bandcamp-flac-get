Function InstallScoopPython {
    Try{
        scoop install python
    }
    Catch [System.Management.Automation.CommandNotFoundException] {
        Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')
        scoop install python
    }
    Write-Host "python has been installed via scoop"
}

Function InitVenv {
    Try{
        python --version
    }
    Catch [System.Management.Automation.CommandNotFoundException] {
        .\windowsInstallPython.ps1
    }
    Finally {
        python -m pip install virtualenv
        python -m virtualenv venv
        .\venv\Scripts\activate
        python -m pip install -r requirements.txt
    }
    
}


InstallScoopPython
InitVenv