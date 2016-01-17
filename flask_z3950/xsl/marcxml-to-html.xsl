<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
   <xsl:output method="html" indent="no" />
   <xsl:variable name="control-num" select="translate(record/controlfield[@tag='001'],
      translate(record/controlfield[@tag='001'], '0123456789', ''), '')" />
   <xsl:template match="record">
      <div class="row marc-record">
         <div class="col-xs-8" id="{$control-num}">
            <p>

               <!-- Title -->
               <a href="#" target="_blank">
                  <xsl:value-of select="concat(datafield[@tag=880]/subfield[@code=6][contains(text(),'245')]
                     /following-sibling::subfield[@code = 'a' or @code = 'b'],' ')" />
                  <xsl:value-of select="concat(datafield[@tag='245']/subfield[@code = 'a' or @code = 'b'],' ')" />
               </a>
               <br />

               <!-- Uniform Title -->
               <xsl:value-of select="concat(datafield[@tag=880]/subfield[@code=6][contains(text(),'240')]
                  /following-sibling::subfield[@code = 'a' or @code = 'b'],' ')" />
               <xsl:value-of select="concat(datafield[@tag='245']/subfield[@code = 'a' or @code = 'b'],' ')" />

               <!-- Author -->
               <xsl:value-of select="concat(datafield[@tag=880]/subfield[@code=6][contains(text(),'100')]
                  /following-sibling::subfield[@code = 'a'],' ')" />
               <xsl:value-of select="concat(datafield[@tag='100']/subfield[@code = 'a'],' ')" />
               <xsl:value-of select="concat(datafield[@tag=880]/subfield[@code=6][contains(text(),'110')]
                  /following-sibling::subfield[@code = 'a'],' ')" />
               <xsl:value-of select="concat(datafield[@tag='110']/subfield[@code = 'a'],' ')" />
               <xsl:value-of select="concat(datafield[@tag=880]/subfield[@code=6][contains(text(),'111')]
                  /following-sibling::subfield[@code = 'a'],' ')" />
               <xsl:value-of select="concat(datafield[@tag='111']/subfield[@code = 'a'],' ')" />
               <br />
               <small>

                  <!-- Publisher -->
                  <xsl:value-of select="concat(datafield[@tag=880]/subfield[@code=6][contains(text(),'260')]
                     /following-sibling::subfield[@code = 'b'],' ')" />
                  <xsl:value-of select="concat(datafield[@tag='260']/subfield[@code = 'b'],' ')" />
                  <xsl:value-of select="concat(datafield[@tag=880]/subfield[@code=6][contains(text(),'264')]
                     /following-sibling::subfield[@code = 'b'],' ')" />
                  <xsl:value-of select="concat(datafield[@tag='264']/subfield[@code = 'b'],' ')" />
                  <xsl:value-of select="concat(datafield[@tag='260']/subfield[@code = 'c'],' ')" />
                  <xsl:value-of select="concat(datafield[@tag='264']/subfield[@code = 'c'],' ')" />
                  <br />

                  <!-- Physical description -->
                  <xsl:value-of select="concat(datafield[@tag='300']/subfield[@code = 'a' or @code = 'b' or @code = 'c' or @code = 'f'],' ')" />
                  <br />
               </small>
            </p>
         </div>

         <!-- Select button -->
         <div class="col-xs-4">
            <a href="#" data-control-num="{$control-num}" class="btn btn-success btn-marc pull-right">Select</a>
         </div>
      </div>
   </xsl:template>
</xsl:stylesheet>